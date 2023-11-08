from typing import Callable
from globals.config import client_version, full_client_version
from globals.externals import pb
from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Label, Input, Static, Button, Tree
from textual.containers import Container, Horizontal, VerticalScroll
from textual import on, work, log
from textual.reactive import reactive
from textual.worker import Worker, WorkerState

from contexts.game_manager import GameManager, StateWrapper
from contexts.connection_manager import FrontdoorChatter, BattlefieldChatter


class ItemTree(Tree):
    """A wrapper to display information in another container"""

    DEFAULT_CSS = "ItemTree { height: auto; }"


from textual.widgets.tree import TreeNode
from rich.console import RenderableType


class MessageQueue(VerticalScroll):
    """A message queue to display begin and end events"""

    def on_mount(self):
        self.queue: dict[RenderableType, TreeNode] = {}

    def add_begin(self, context: RenderableType, parent=""):
        if parent != "" and parent in self.queue:
            self.queue[context] = self.queue[parent].add(context + " loading ...")
        elif context not in self.queue:
            tree = ItemTree(context + " loading ...")
            self.queue[context] = tree.root
            self.queue[context].expand()
            self.mount(tree)
        self.scroll_end(animate=False)

    def add_end(self, context: RenderableType, payload=None):
        if context in self.queue:
            self.queue[context].set_label(context + " finished!")
            if payload != None:
                match payload:
                    case str():
                        self.queue[context].add_leaf(payload)
                    case dict():
                        from rich.json import JSON

                        # TODO
                        self.queue[context].add_leaf(str(payload))
                    case _:
                        self.queue[context].add_leaf(str(payload))
            self.queue.pop(context)
        self.scroll_end(animate=False)

    def add_fail(self, context: RenderableType):
        if context in self.queue:
            for label in [
                label
                for label, node in self.queue.items()
                for child in self.queue[context].children
                if child == node
            ]:
                self.add_fail(label)
            self.queue[context].set_label(context + " failed!")
            self.queue.pop(context)

    def add_message(self, context: str, parent=""):
        if parent != "" and parent in self.queue:
            self.queue[parent].add_leaf(Static(context))
        else:
            self.mount(Static(context))


class MtgShow(App):
    CSS = """
Screen {
    background: #212529;
}
"""

    def compose(self) -> ComposeResult:
        with MessageQueue(id="message_queue"):
            yield Static("UI instantiated.")
        with Input(placeholder="Enter your message", id="message_input") as input:
            input.focus()

    async def on_mount(self):
        self.query_one(Input).focus()
        self.bf_state_updater = self.set_interval(
            4, self.update_state, name="updater", pause=True
        )
        self.last_input = None
        self.log_file = open("log.txt", "w+")

        def init_queue():
            try:
                yield self.yielder_submit(self.load_front_door_yielder)
                yield self.yielder_submit(self.auth_yielder)
                yield self.yielder_submit(self.join_yielder)
                yield self.yielder_submit(self.authduel_yielder)
                yield self.yielder_submit(self.connect_room_yielder)
            except:
                pass

        self.init_queue = init_queue()
        next(self.init_queue, None)

    async def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """see https://github.com/Textualize/textual/discussions/3174"""
        if event.state == WorkerState.SUCCESS:
            if hasattr(self, "init_queue") and self.init_queue:
                if not next(self.init_queue, None):
                    self.__delattr__("init_queue")
        elif event.state == WorkerState.ERROR:
            if hasattr(self, "init_queue"):
                self.__delattr__("init_queue")

    @work(thread=True, exit_on_error=False)
    async def yielder_submit(self, yielder):
        mq = self.query_one(MessageQueue)
        last_message = ""
        self.call_from_thread(mq.add_begin, yielder.__name__)
        from requests import ConnectTimeout

        full_message = None
        for message in self.call_from_thread(yielder):
            match message:
                case (summary, payload):
                    message = summary
                    full_message = payload
                case e if isinstance(e, Exception):
                    self.call_from_thread(mq.add_fail, yielder.__name__)
                    raise e
                case s if isinstance(s, str):
                    full_message = None
            if last_message != "":
                self.call_from_thread(mq.add_end, last_message, payload=full_message)
            self.call_from_thread(mq.add_begin, message, parent=yielder.__name__)
            last_message = message
        self.call_from_thread(mq.add_end, last_message)
        self.call_from_thread(mq.add_end, yielder.__name__)

    def load_front_door_yielder(self):
        from utils import ring_doorbell, fast_login

        yield "ring doorbell"
        fd_uri = ring_doorbell()
        yield "fast log-in", fd_uri
        try:
            account_info = fast_login()
        except Exception as e:
            yield e
            return
        yield "parse info", account_info
        self.access_token = account_info["access_token"]
        self.refresh_token = account_info["refresh_token"]
        self.persona_id = account_info["persona_id"]
        from urllib.parse import urlparse

        parse_result = urlparse(fd_uri)

        yield "init front door connection"
        self.fd_chatter = FrontdoorChatter(
            parse_result.hostname, parse_result.port, "cert.pem"
        )
        try:
            self.fd_chatter.__enter__()
        except Exception as e:
            yield e
            return
        yield "init battlefield connection"
        self.bf_chatter = BattlefieldChatter(
            None, None, "./cert.pem", client_version, None, None, timeout=0.2
        )

    @on(Input.Submitted)
    def on_input_message_submitted(self, event: Input.Submitted) -> None:
        self.last_input = event.value
        message_input = self.query_one("#message_input", Input)
        with message_input.prevent(Input.Changed):
            message_input.value = ""
        if event.value:
            self.submit(event.value)

    def add_message(self, msg: str):
        mq = self.query_one(MessageQueue)
        mq.add_message(msg)

    def submit(self, command: str) -> None:
        method_of_this = command + "_yielder"
        if hasattr(self, method_of_this) and callable(
            func := getattr(self, method_of_this)
        ):
            self.yielder_submit(func)
        else:
            try:
                eval(command)
            except SyntaxError:
                pass

    def auth_yielder(self):
        yield "authenticate to battlefield"
        self.fd_chatter.authenticate(full_client_version, self.access_token)

    def join_yielder(self):
        yield "joining match"
        self.fd_chatter.join_match()
        yield "getting credentials"
        self.bf_chatter.fabric_uri = self.fd_chatter.controller_fabric_uri
        self.bf_chatter.match_id = self.fd_chatter.match_id
        self.bf_chatter.host = self.fd_chatter.match_endpoint_host
        self.bf_chatter.port = self.fd_chatter.match_endpoint_port
        self.bf_chatter.__enter__()

    def authduel_yielder(self):
        if hasattr(self, "bf_chatter") and self.bf_chatter.sock:
            yield "send authenticate duel message"
            trans_id = self.bf_chatter.propose(
                pb.ClientToMatchServiceMessageType.ClientToMatchServiceMessageType_AuthenticateRequest,
                pb.AuthenticateRequest(
                    clientId=self.persona_id,
                    playFabSessionTicket=self.access_token,
                    inactivityTimeoutMs=60000,
                    clientInfo=pb.ClientInfo(
                        clientType=pb.ClientType.ClientType_User,
                        clientVersion=client_version,
                    ),
                ),
            )

            yield "receive reply"
            for _ in range(20):
                self.bf_chatter.admit()
                if (
                    trans_id in self.bf_chatter.reply
                    and self.bf_chatter.reply[trans_id]
                ):
                    log(self.bf_chatter.reply[trans_id])
                    break
            if trans_id not in self.bf_chatter.reply:
                return
            yield "setting game manager", self.bf_chatter.reply[trans_id][0]
            self.game_manager = GameManager(self.bf_chatter, self.log_file, None)
            self.bf_state_updater.resume()
            yield "all done"

    def update_state(self):
        state = None
        reply = None
        try:
            state, reply = self.game_manager.update(self.last_input)
            self.last_input = None
        except TimeoutError:
            self.state_str.update("disconnected")
            if hasattr(self, "bf_chatter") and self.bf_chatter:
                self.bf_chatter.__exit__()
            self.bf_state_updater.pause()
            return
        except Exception as e:
            log(f"there is an error {e}")
            return

        if reply:
            trans_id = self.bf_chatter.propose(
                pb.ClientToMatchServiceMessageType.ClientToMatchServiceMessageType_ClientToGREMessage,
                reply,
            )

        def update_state_str(state: StateWrapper):
            from contexts.card_oracle import query

            def query_name(id: int) -> str:
                return tup[0] if (tup := query(id)) else "unknown"

            my_hand = [
                query_name(instance.overlay_grp_id)
                for instance in state.get_zone_cards("ZoneType_Hand")
            ]
            opponent_hand = len(state.get_zone_cards("ZoneType_Hand", False))
            my_deck = len(state.get_zone_cards("ZoneType_Library"))
            opponent_deck = len(state.get_zone_cards("ZoneType_Library", False))
            my_grave = len(state.get_zone_cards("ZoneType_Graveyard"))
            opponent_grave = len(state.get_zone_cards("ZoneType_Graveyard", False))
            my_exile = len(state.get_zone_cards("ZoneType_Exile"))
            opponent_exile = len(state.get_zone_cards("ZoneType_Exile", False))
            the_field = [
                query_name(instance.overlay_grp_id)
                for instance in state.get_zone_cards("ZoneType_Battlefield", None)
            ]
            the_stack = [
                query_name(instance.overlay_grp_id)
                for instance in state.get_zone_cards("ZoneType_Stack", None)
            ]

            self.state_str.update(
                f"your hand: {my_hand}\n"
                f"the field: {the_field}\n"
                f"the stack: {the_stack}\n"
                f"your opponent's hand: {opponent_hand}\n"
                f"your deck: {my_deck}\n"
                f"your opponent's deck: {opponent_deck}\n"
                f"your GY: {my_grave}\n"
                f"your oppenent's GY: {opponent_grave}\n"
                f"your exile: {my_exile}\n"
                f"your opponent's exile: {opponent_exile}\n"
                f"options:\n{self.game_manager.get_available_options()}"
            )

        if not hasattr(self, "recorder"):
            self.recorder = VerticalScroll()
            self.mount(self.recorder)
            self.state_str = Static()
            self.recorder.mount(self.state_str)
        if state:
            try:
                update_state_str(state)
            except Exception as e:
                log(e)

    def connect_room_yielder(self):
        if hasattr(self, "bf_chatter") and self.bf_chatter.sock:
            yield "connecting to room"
            trans_id = self.bf_chatter.propose(
                pb.ClientToMatchServiceMessageType.ClientToMatchServiceMessageType_ClientToMatchDoorConnectRequest,
                self.bf_chatter.construct_door_connect_request(),
            )
            yield "all done", trans_id

    def state_yielder(self):
        if hasattr(self, "bf_chatter") and self.bf_chatter.sock:
            yield "retrieve state message"
            yield "add tail?", self.bf_chatter.get_gre_client_messages()

    def reconnect_yielder(self):
        yield "cleaning connections"
        if hasattr(self, "fd_chatter"):
            self.fd_chatter.__exit__()
        yield "reconnecting"
        for msg in self.load_front_door_yielder():
            yield msg

    def on_exit(self):
        self.fd_chatter.__exit__()
        self.log_file.close()
        if hasattr(self.bf_chatter, "__enter__"):
            self.bf_chatter.__exit__()

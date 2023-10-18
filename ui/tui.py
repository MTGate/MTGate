from globals.config import client_version, full_client_version
from globals.externals import pb
from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Label, Input, Static, Button
from textual.containers import Container, Horizontal
from textual import on, work, log
from textual.reactive import reactive

from contexts.connection_manager import FrontdoorChatter, BattlefieldChatter

class FocusableContainer(Container, can_focus=True):
    """Focusable container widget."""

class MessageBox(Widget, can_focus=True):
    def __init__(self, text: str) -> None:
        self.text = text
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Static(self.text)

class MtgShow(App):
    CSS = '''
Screen {
    background: #212529;
}

MessageBox {
    layout: horizontal;
    height: auto;
    align-horizontal: center;
}

.message {
    width: auto;
    min-width: 25%;
    border: tall black;
    padding: 1 3;
    margin: 1 0;
    background: #343a40;
}
#input_box {
    dock: bottom;
    height: 20%;
    width: 70%;
    margin: 0 0 2 0;
    background: red 10%;
    align_horizontal: right;
}
'''
    def compose(self) -> ComposeResult:
        with FocusableContainer(id="conversation_box"):
            yield MessageBox(
                "UI instantiated, waiting for connection ..."
            )
        with Horizontal(id="input_box"):
            yield Input(placeholder="Enter your message", id="message_input")

    def add_message(self, message: str):
        conversation_box = self.query_one("#conversation_box")
        conversation_box.mount(MessageBox(message))
        conversation_box.scroll_end(animate=False)

    async def on_mount(self):
        self.load_front_door()
        self.query_one(Input).focus()

    @work(thread=True)
    def load_front_door(self) -> bool:
        from requests import ConnectTimeout
        try:
            from utils import ring_doorbell, fast_login
            fd_uri = ring_doorbell()
            account_info = fast_login()
            self.access_token = account_info["access_token"]
            self.refresh_token = account_info["refresh_token"]
            self.persona_id = account_info["persona_id"]
            from urllib.parse import urlparse
            parse_result = urlparse(fd_uri)

            self.fd_chatter = FrontdoorChatter(parse_result.hostname, parse_result.port, 'cert.pem')
            self.fd_chatter.__enter__()
            self.bf_chatter = BattlefieldChatter(None, None, './cert.pem', client_version, None, None)
            self.call_from_thread(self.add_message, "load front door successfully!")
        except (ConnectTimeout, TimeoutError):
            self.call_from_thread(self.add_message, "failed to load front door.")
    
    @on(Input.Submitted)
    def consult(self, event: Input.Submitted) -> None:
        message_input = self.query_one("#message_input", Input)
        with message_input.prevent(Input.Changed):
            message_input.value = ""
        if event.value:
            self.submit(event.value)
    
    @work(thread=True)
    async def submit(self, command: str) -> None:
        match command:
            case "auth":
                self.call_from_thread(self.add_message, "authenticating using your access token ...")
                self.call_from_thread(
                    self.add_message,
                    self.fd_chatter.authenticate(full_client_version,
                                                self.access_token)
                )
            case "join":
                self.call_from_thread(self.add_message, "joining match ...")
                self.call_from_thread(
                    self.add_message,
                    self.fd_chatter.join_match()
                )
                self.bf_chatter.fabric_uri = self.fd_chatter.controller_fabric_uri
                self.bf_chatter.match_id = self.fd_chatter.match_id
                self.bf_chatter.host = self.fd_chatter.match_endpoint_host
                self.bf_chatter.port = self.fd_chatter.match_endpoint_port
                self.bf_chatter.__enter__()
            # case "auth_duel":
                if hasattr(self, "bf_chatter") and self.bf_chatter.sock:
                    self.call_from_thread(self.add_message, "authenticating duel ...")
                    trans_id = self.bf_chatter.propose(
                        pb.ClientToMatchServiceMessageType.ClientToMatchServiceMessageType_AuthenticateRequest,
                        pb.AuthenticateRequest(
                            clientId=self.persona_id,
                            playFabSessionTicket=self.access_token,
                            inactivityTimeoutMs=60000,
                            clientInfo=pb.ClientInfo(
                                clientType=pb.ClientType.ClientType_User,
                                clientVersion=client_version
                            )
                        )
                    )
                    
                    def update_bf_message():
                        self.bf_chatter.admit()
                        if trans_id in self.bf_chatter.reply:
                            self.add_message("Duel access authenticated!")
                            log(self.bf_chatter.reply[trans_id])
                            self.update_bf_message.pause()
                    self.update_bf_message = self.call_from_thread(self.set_interval,
                                                                   1, update_bf_message, repeat=20
                                                                   )
            case "connect_room":
                if hasattr(self, "bf_chatter") and self.bf_chatter.sock:
                    self.call_from_thread(self.add_message, "connecting to room ...")
                    trans_id = self.bf_chatter.propose(
                        pb.ClientToMatchServiceMessageType.ClientToMatchServiceMessageType_ClientToMatchDoorConnectRequest,
                        self.bf_chatter.construct_door_connect_request()
                    )

                    cnt = [0]
                    def update_bf_message(cnt=cnt):
                        self.bf_chatter.admit()
                        if trans_id in self.bf_chatter.reply:
                            self.add_message("Room state updated!")
                            self.add_message(self.bf_chatter.reply[trans_id][cnt[0]])
                            cnt[0] += 1
                            if cnt[0] >= 2:
                                self.update_bf_message.pause()
                    self.update_bf_message = self.call_from_thread(self.set_interval,
                                                                   1, update_bf_message, repeat=20
                                                                   )
            case "state":
                if hasattr(self, "bf_chatter") and self.bf_chatter.sock:
                    self.call_from_thread(self.add_message, "retrieving state ...")
                    self.call_from_thread(
                        self.add_message,
                        self.bf_chatter.get_gre_client_messages()
                    )
            case "reconnect":
                self.call_from_thread(self.add_message, "reloading connection ...")
                if hasattr(self, "fd_chatter"):
                    self.fd_chatter.__exit__()
                self.load_front_door()

    def on_exit(self):
        self.fd_chatter.__exit__()
        if hasattr(self.bf_chatter, "__enter__"):
            self.bf_chatter.__exit__()
from globals.config import client_version, full_client_version
from globals.externals import pb
from textual.app import App, ComposeResult
from textual.widgets import Input, Static, TabbedContent, TabPane
from textual.containers import VerticalScroll
from textual import on, work, log
from textual.worker import Worker, WorkerState

from contexts.game_manager import GameManager, StateWrapper
from contexts.connection_manager import FrontdoorChatter, BattlefieldChatter
from tui.message_queue import MessageQueue


class TaskPanel(TabPane):
    def __init__(
        self,
        connection=None,
        title: str | None = None,
        id: str | None = None,
    ) -> None:
        super().__init__(title, id=id)
        self.connection = connection
        self.input_queue = []
        self.output_queue = []

    def on_mount(self):
        self.mount(VerticalScroll(Static(f"{self._title} initialized")))

    # def update_state()

    # def on_unmount(self):
    #     log(111)


class MtgOffline(App):
    CSS = """
Screen {
    background: #212529;
}
"""

    def compose(self) -> ComposeResult:
        with TabbedContent(initial="log_state"):
            with TabPane("Logs", id="log_state"):
                with MessageQueue(id="message_queue"):
                    yield Static("UI instantiated.")
        with Input(placeholder="Enter your message", id="message_input") as input:
            input.focus()

    async def on_mount(self):
        self.query_one(Input).focus()
        self.last_input = None
        self.log_file = open("log.txt", "w+")

        def init_queue():
            yield self.yielder_submit(self.load_1_yielder)
            yield self.yielder_submit(self.load_2_yielder)

        self.init_queue = init_queue()
        next(self.init_queue, None)

    async def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
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

    def load_1_yielder(self):
        self.load_1 = TaskPanel(title="123", id="_123")
        tc = self.query_one(TabbedContent)
        tc.add_pane(self.load_1)
        tc.active = "_123"
        yield "done"

    def load_2_yielder(self):
        import time

        time.sleep(10)
        self.load_2 = TaskPanel(title="1234", id="_1234")
        tc = self.query_one(TabbedContent)
        tc.add_pane(self.load_2)
        tc.active = "_1234"
        yield "done"

    def on_unmount(self):
        self.log_file.close()


class TestApp(App):
    def compose(self) -> ComposeResult:
        yield TabbedContent()
        yield Input()

    async def on_mount(self):
        self.async_caller()
        # self.slow_init()

    @work(thread=True)
    async def async_caller(self):
        self.call_from_thread(self.slow_init)
        # self.slow_init()

    def slow_init(self):
        import time

        time.sleep(10)
        tc = self.query_one(TabbedContent)
        tp = TabPane("1234", id="_1234")
        tc.add_pane(tp)
        tp.mount(VerticalScroll(Static("111")))

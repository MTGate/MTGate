from textual.app import App, ComposeResult
from textual.widgets import Label, Input
from textual import on, work
from textual.reactive import reactive

from contexts.connection_manager import FrontdoorChatter, BattlefieldChatter

class MtgShow(App):

    CSS = """
    Label {
        margin:1 1;
        height: 80%;
        width: 100%;
        background: $panel;
        border: tall $primary;
        content-align: center middle;
    }
    Input {
        height: 10%;
    }
    """

    message = reactive("waiting for front door ...")

    def set_message(self, message):
        self.message = message

    async def on_mount(self):
        self.load_front_door()

    @work(exclusive=True, thread=True)
    def load_front_door(self) -> bool:
        from requests import ConnectTimeout
        try:
            from utils import ring_doorbell, fast_login
            from globals.config import client_version, full_client_version
            fd_uri = ring_doorbell()
            account_info = fast_login()
            self.access_token = account_info["access_token"]
            self.refresh_token = account_info["refresh_token"]
            self.full_client_version = full_client_version
            from urllib.parse import urlparse
            parse_result = urlparse(fd_uri)

            self.fd_chatter = FrontdoorChatter(parse_result.hostname, parse_result.port, 'cert.pem')
            self.fd_chatter.__enter__()
            self.bf_chatter = BattlefieldChatter(None, None, './cert.pem', client_version, None, None)
            self.call_from_thread(self.set_message, "load front door successfully!")
        except ConnectTimeout:
            self.call_from_thread(self.set_message, "failed to load front door.")

    def watch_message(self):
        self.query_one(Label).update(self.message)

    def compose(self) -> ComposeResult:
        yield Label()
        yield Input(placeholder="input your command here")
    
    @on(Input.Submitted)
    def consult(self, event: Input.Submitted) -> None:
        if event.value and not (hasattr(self, "bf_chatter") and hasattr(self.bf_chatter, "__enter__")):
            self.submit(event.value)
        self.query_one(Input).clear()
    
    @work(exclusive=True, thread=True)
    async def submit(self, command: str) -> None:
        match command:
            case "auth":
                self.call_from_thread(self.set_message, "authenticating using your access token ...")
                self.watch_message()
                self.call_from_thread(
                    self.set_message,
                    self.fd_chatter.authenticate(self.full_client_version,
                                                self.access_token)
                )
                self.watch_message()
            case "join":
                self.call_from_thread(self.set_message, "joining match ...")
                self.watch_message()
                self.call_from_thread(
                    self.set_message,
                    self.fd_chatter.join_match()
                )
                self.watch_message()
                self.bf_chatter.fabric_uri = self.fd_chatter.controller_fabric_uri
                self.bf_chatter.match_id = self.fd_chatter.match_id
                self.bf_chatter.host = self.fd_chatter.match_endpoint_host
                self.bf_chatter.port = self.fd_chatter.match_endpoint_port
                self.bf_chatter.__enter__()
            case "reconnect":
                self.__exit__()
                self.load_front_door()
            

    def on_exit(self):
        self.fd_chatter.__exit__()
        if hasattr(self.bf_chatter, "__enter__"):
            self.bf_chatter.__exit__()
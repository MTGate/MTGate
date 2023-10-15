from textual.app import App, ComposeResult
from textual.widgets import Label, Input
from textual import on, work
from textual.reactive import reactive

from contexts.state_manager import state
from contexts.connection_manager import FrontdoorChatter

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

    def on_mount(self):
        from utils import ring_doorbell, fast_login
        from globals.config import full_client_version

        fd_uri = ring_doorbell()
        account_info = fast_login()
        self.access_token = account_info["access_token"]
        self.refresh_token = account_info["refresh_token"]
        self.full_client_version = full_client_version
        from urllib.parse import urlparse
        parse_result = urlparse(fd_uri)

        self.chatter = FrontdoorChatter(parse_result.hostname, parse_result.port, 'cert.pem')
        self.chatter.__enter__()

    def update_text(self, text):
        self.query_one(Label).update(text)

    def compose(self) -> ComposeResult:
        yield Label()
        yield Input(placeholder="input your command here")
    
    @on(Input.Submitted)
    def consult(self, event: Input.Submitted) -> None:
        if event.value:
            self.submit(event.value)
    
    @work(exclusive=True)
    async def submit(self, command: str) -> None:
        match command:
            case "authenticate":
                self.update_text(self.chatter.authenticate(self.full_client_version,
                                                            self.access_token))
            case "join match":
                self.update_text(self.chatter.join_match())

    def on_exit(self):
        self.chatter.__exit__()
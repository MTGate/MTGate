from textual.app import App, ComposeResult
from textual.widgets import Label, Input
from textual import on

NAMES = [
    "Paul Atreidies",
    "Duke Leto Atreides",
    "Lady Jessica",
    "Gurney Halleck",
    "Baron Vladimir Harkonnen",
    "Glossu Rabban",
    "Chani",
    "Silgar",
]


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

    def __init__(self, submitter, displayer):
        super.__init__(self)
        self.submitter = submitter
        self.displayer = displayer

    def compose(self) -> ComposeResult:
        yield Label()
        yield Input(placeholder="input your command here")
    
    @on(Input.Submitted)
    def consult(self, event: Input.Submitted) -> None:
        self.submitter(event.value)

    
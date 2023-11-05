from contexts.card_oracle import query
from textual.widgets import Label


class NameCard(Label):
    def __init__(self, id: str):
        name, ty, oracle = query(id)
        super().__init__(name)
        self.tooltip = f"{name}\n\n{ty}\n\n{oracle}"

from textual.widgets import Static, Tree
from textual.containers import VerticalScroll


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

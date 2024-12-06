from __future__ import annotations

from rich.style import Style
from rich.text import Text, TextType
from textual.binding import Binding
from textual.widgets import Tree
from textual.widgets._tree import TreeNode

from ..schemas import CommandName, CommandSchema


class CommandTree(Tree[CommandSchema]):
    COMPONENT_CLASSES = {"group"}

    BINDINGS = [
        Binding("enter", "focus_next", "", priority=True, show=False),
        Binding("j", "cursor_down", "", priority=True, show=False),
        Binding("k", "cursor_up", "", priority=True, show=False),
        Binding("g", "scroll_home", "", priority=True, show=False),
        Binding("G", "scroll_end", "", priority=True, show=False),
        Binding("u", "page_up", "", priority=True, show=False),
        Binding("d", "page_down", "", priority=True, show=False),
    ]

    def __init__(
        self,
        label: TextType,
        cli_metadata: dict[CommandName, CommandSchema],
    ):
        super().__init__(label)
        self.show_root = False
        self.guide_depth = 2
        self.show_guides = False
        self.cli_metadata = cli_metadata

    def render_label(
        self,
        node: TreeNode[CommandSchema],
        base_style: Style,
        style: Style,
    ) -> Text:
        label = node._label.copy()
        label.stylize(style)
        return label

    def on_mount(self):
        def build_tree(
            data: dict[CommandName, CommandSchema],
            node: TreeNode[CommandSchema],
        ) -> TreeNode[CommandSchema]:
            data = {key: data[key] for key in sorted(data)}
            for cmd_name, cmd_data in data.items():
                if cmd_data.subcommands:
                    label = Text(cmd_name)
                    group_style = self.get_component_rich_style("group")
                    label.stylize(group_style)
                    child = node.add(label, allow_expand=False, data=cmd_data)
                    build_tree(cmd_data.subcommands, child)
                else:
                    node.add_leaf(cmd_name, data=cmd_data)
            return node

        build_tree(self.cli_metadata, self.root)
        self.root.expand_all()
        self.select_node(self.root)

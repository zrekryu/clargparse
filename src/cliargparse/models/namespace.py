from __future__ import annotations

from typing import TYPE_CHECKING, Any


if TYPE_CHECKING:
    from cliargparse.parser.nodes import CommandNode


class Namespace(dict[str, Any]):
    @classmethod
    def from_node(cls, node: CommandNode) -> Namespace:
        namespace = cls()

        for option, option_node in node.options.items():
            namespace[option.store_name] = option_node.values

        if subcommand_node := node.subcommand:
            namespace[subcommand_node.command.name] = cls.from_node(subcommand_node)

        for positional, positional_node in node.positionals.items():
            namespace[positional.name] = positional_node.values

        return namespace

    def __repr__(self) -> str:
        items_repr = ", ".join(f"{key}={value!r}" for key, value in self.items())
        return f"{type(self).__name__}({items_repr})"

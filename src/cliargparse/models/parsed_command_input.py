from __future__ import annotations

from typing import TYPE_CHECKING

from .parsed_values import ParsedValues


if TYPE_CHECKING:
    from cliargparse.parser.nodes import CommandNode, OptionNode, PositionalNode


class ParsedCommandInput:
    def __init__(
        self,
        node: CommandNode,
        value_to_node: dict[str, CommandNode | OptionNode | PositionalNode],
        values: ParsedValues,
    ) -> None:
        self.node = node
        self.value_to_node = value_to_node
        self.values = values

    @classmethod
    def from_node(cls, node: CommandNode) -> ParsedCommandInput:
        value_to_node: dict[str, CommandNode | OptionNode | PositionalNode] = {}
        values = ParsedValues()

        for option in node.command.options:
            if option_node := node.options.get(option):
                value_to_node[option.store_name] = option_node
                values[option.store_name] = option_node.values
            elif option.default is not None:
                values[option.store_name] = option.default

        if subcommand_node := node.subcommand:
            value_to_node[subcommand_node.command.name] = subcommand_node
            values[subcommand_node.command.name] = cls.from_node(subcommand_node)

        for positional, positional_node in node.positionals.items():
            value_to_node[positional.name] = positional_node
            values[positional.name] = positional_node.values

        return ParsedCommandInput(node, value_to_node, values)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(node={self.node}, values={self.values})"

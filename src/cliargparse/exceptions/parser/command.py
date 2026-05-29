from __future__ import annotations

from typing import TYPE_CHECKING, override

from .base import ParserError


if TYPE_CHECKING:
    from collections.abc import Sequence

    from cliargparse.models.parameters import Command


class UnknownCommandError(ParserError):
    def __init__(self, name: str) -> None:
        super().__init__(name)

        self.name = name

    @override
    def __str__(self) -> str:
        return f"unknown command: {self.name}"


class SubcommandRequiredError(ParserError):
    def __init__(
        self,
        name: str,
        subcommands: Sequence[Command],
    ) -> None:
        super().__init__(name, subcommands)

        self.name = name
        self.subcommands = subcommands

    @override
    def __str__(self) -> str:
        subcommands = ", ".join(subcommand.name for subcommand in self.subcommands)
        return f"command {self.name!r} requires a subcommand (subcommands: {subcommands})"

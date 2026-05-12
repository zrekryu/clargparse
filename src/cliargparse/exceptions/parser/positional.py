from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import ParserError


if TYPE_CHECKING:
    from collections.abc import Sequence

    from cliargparse.enums import NArgs
    from cliargparse.models.parameters import Positional


class MissingPositionalArgumentsError(ParserError):
    def __init__(
        self,
        name: str,
        nargs: int | NArgs,
        received_nargs: int,
    ) -> None:
        super().__init__(name, nargs, received_nargs)

        self.name = name
        self.nargs = nargs
        self.received_nargs = received_nargs

    def __str__(self) -> str:
        s = "s" if isinstance(self.nargs, int) and self.nargs != 1 else ""

        return (
            f"positional {self.name!r} expected {self.nargs} argument{s}, got {self.received_nargs}"
        )


class UnexpectedPositionalArgumentError(ParserError):
    def __init__(self, argument: Sequence[str]) -> None:
        super().__init__(argument)

        self.argument = argument

    def __str__(self) -> str:
        return f"unexpected positional argument {self.argument!r}"


class InvalidPositionalChoiceError(ParserError):
    def __init__(
        self,
        name: str,
        choice: str,
        choices: Sequence[str],
    ) -> None:
        super().__init__(name, choice, choices)

        self.name = name
        self.choice = choice
        self.choices = choices

    def __str__(self) -> str:
        return (
            f"invalid choice {self.choice!r} "
            f"for positional {self.name!r} "
            f"(choices: {', '.join(self.choices)})"
        )


class MissingRequiredPositionalsError(ParserError):
    def __init__(
        self,
        positionals: Sequence[Positional[Any]],
    ) -> None:
        super().__init__(positionals)

        self.positionals = positionals

    def __str__(self) -> str:
        return (
            "missing required positionals: "
            f"{', '.join(repr(positional.name) for positional in self.positionals)}"
        )

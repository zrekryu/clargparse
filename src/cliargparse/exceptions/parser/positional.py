from __future__ import annotations

from typing import TYPE_CHECKING, Any, assert_never

from cliargparse import numargs

from .base import ParserError


if TYPE_CHECKING:
    from collections.abc import Sequence

    from cliargparse.models.parameters import Positional


class MissingPositionalArgumentsError(ParserError):
    def __init__(
        self,
        name: str,
        num_args: int | numargs.BaseNumArgs,
        received_num_args: int,
    ) -> None:
        super().__init__(name, num_args, received_num_args)

        self.name = name
        self.num_args = num_args
        self.received_num_args = received_num_args

    def __str__(self) -> str:
        match self.num_args:
            case numargs.BaseNumArgs():
                expected = self.num_args.cardinality_repr
            case int():
                expected = f"argument{'s' if self.num_args != 1 else ''}"
            case _:
                assert_never(self.num_args)

        return f"option {self.name!r} expected {expected}, got {self.received_num_args}"


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

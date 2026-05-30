from __future__ import annotations

from typing import TYPE_CHECKING, Any, assert_never, override

from clargparse import numargs
from clargparse.enums import OptionPrefix

from .base import ParserError


if TYPE_CHECKING:
    from collections.abc import Sequence

    from clargparse.models import MutexOptionGroup
    from clargparse.models.parameters import Option


class UnknownOptionError(ParserError):
    def __init__(self, specifier: str) -> None:
        super().__init__(specifier)

        self.specifier = specifier

    @override
    def __str__(self) -> str:
        return f"unknown option: {self.specifier}"


class UnknownLongOptionError(UnknownOptionError):
    def __init__(self, name: str) -> None:
        super().__init__(f"{OptionPrefix.LONG}{name}")

        self.name = name

    @override
    def __str__(self) -> str:
        return f"unknown long option: {self.specifier}"


class UnknownShortOptionError(UnknownOptionError):
    def __init__(self, name: str) -> None:
        super().__init__(f"{OptionPrefix.SHORT}{name}")

        self.name = name

    @override
    def __str__(self) -> str:
        return f"unknown short option: {self.specifier}"


class UnknownShortOptionInGroupError(UnknownShortOptionError):
    def __init__(self, name: str, group: str) -> None:
        super().__init__(name)

        self.group = group

    @override
    def __str__(self) -> str:
        return f"unknown short option {self.name!r} in group {self.group!r}"


class OptionTakesNoArgumentsError(ParserError):
    def __init__(self, specifier: str, argument: str) -> None:
        super().__init__(specifier, argument)

        self.specifier = specifier
        self.argument = argument

    @override
    def __str__(self) -> str:
        return f"option {self.specifier!r} takes no argument, but got {self.argument!r}"


class OptionTakingArgumentInGroupError(ParserError):
    def __init__(self, name: str, group: str) -> None:
        super().__init__(name, group)

        self.name = name
        self.group = group

    @override
    def __str__(self) -> str:
        return (
            f"option {self.name!r} in group "
            f"'{OptionPrefix.SHORT}{self.group}' "
            "must not take an argument"
        )


class MissingOptionArgumentsError(ParserError):
    def __init__(
        self,
        specifier: str,
        num_args: int | numargs.BaseNumArgs,
        received_num_args: int,
    ) -> None:
        super().__init__(specifier, num_args, received_num_args)

        self.specifier = specifier
        self.num_args = num_args
        self.received_num_args = received_num_args

    @override
    def __str__(self) -> str:
        match self.num_args:
            case numargs.BaseNumArgs():
                expected = self.num_args.expected_cardinality_repr
            case int():
                expected = f"argument{'s' if self.num_args != 1 else ''}"
            case _:
                assert_never(self.num_args)

        return f"option {self.specifier!r} expected {expected}, got {self.received_num_args}"


class InvalidOptionChoiceError(ParserError):
    def __init__(
        self,
        specifier: str,
        choice: str,
        choices: Sequence[str],
    ) -> None:
        super().__init__(specifier, choice, choices)

        self.specifier = specifier
        self.choice = choice
        self.choices = choices

    @override
    def __str__(self) -> str:
        return (
            f"invalid choice {self.choice!r} "
            f"for option {self.specifier!r} "
            f"(choices: {', '.join(self.choices)})"
        )


class MissingRequiredOptionsError(ParserError):
    def __init__(self, options: Sequence[Option[Any]]) -> None:
        super().__init__(options)

        self.options = options

    @override
    def __str__(self) -> str:
        return (
            f"missing required options: {', '.join(option.display_name for option in self.options)}"
        )


class MutexOptionCannotCoexistError(ParserError):
    def __init__(self, specifier: str, conflicts: Sequence[str]) -> None:
        self.specifier = specifier
        self.conflicts = conflicts

    @override
    def __str__(self) -> str:
        conflicts = ", ".join(map(repr, self.conflicts))
        return f"option {self.specifier!r} cannot coexist with {conflicts}"


class MissingRequiredMutexOptionFromGroupError(ParserError):
    def __init__(self, group: MutexOptionGroup) -> None:
        self.group = group

    @override
    def __str__(self) -> str:
        options = ", ".join(option.display_name for option in self.group.options)
        return f"one of the mutually exclusive options ({options}) is required"

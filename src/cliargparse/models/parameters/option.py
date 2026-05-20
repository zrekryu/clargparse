from __future__ import annotations

from dataclasses import KW_ONLY, dataclass
from typing import TYPE_CHECKING, assert_never

from cliargparse import numargs
from cliargparse.actions import (
    append_present_action,
    count_presence_action,
    store_false_action,
    store_present_action,
    store_true_action,
    store_value_action,
)
from cliargparse.enums import OptionPrefix

from .parameter import Parameter


if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from cliargparse.hints import Action


@dataclass(frozen=True)
class Option[T](Parameter):
    long_names: tuple[str, ...]
    short_names: tuple[str, ...]

    _: KW_ONLY

    long_aliases: tuple[str, ...]
    short_aliases: tuple[str, ...]

    store_name: str

    action: Action[Option[T]]
    num_args: int | numargs.BaseNumArgs

    default: T | None = None
    present: T | None = None

    type_converter: type[str] | Callable[[str], T]
    choices: tuple[T, ...]
    required: bool

    @property
    def names(self) -> tuple[str, ...]:
        return self.all_long_names + self.all_short_names

    @property
    def all_long_names(self) -> tuple[str, ...]:
        return self.long_names + self.long_aliases

    @property
    def all_short_names(self) -> tuple[str, ...]:
        return self.short_names + self.short_aliases

    @property
    def specifiers(self) -> tuple[str, ...]:
        return self.long_specifiers + self.short_specifiers

    @property
    def long_specifiers(self) -> tuple[str, ...]:
        return tuple(f"{OptionPrefix.LONG}{name}" for name in self.all_long_names)

    @property
    def short_specifiers(self) -> tuple[str, ...]:
        return tuple(f"{OptionPrefix.SHORT}{name}" for name in self.all_short_names)

    @property
    def display_name(self) -> str:
        if self.long_names:
            display_name = f"{OptionPrefix.LONG}{self.long_names[0]}"

            if self.short_names:
                display_name += f"/{OptionPrefix.SHORT}{self.short_names[0]}"

            return display_name

        return f"{OptionPrefix.SHORT}{self.short_names[0]}"

    @property
    def takes_arguments(self) -> bool:
        match self.num_args:
            case numargs.BaseNumArgs():
                return True
            case int():
                return self.num_args > 0
            case _:
                assert_never(self.num_args)

    @classmethod
    def create(
        cls,
        long_names: str | Sequence[str] | None = None,
        short_names: str | Sequence[str] | None = None,
        *,
        long_aliases: str | Sequence[str] | None = None,
        short_aliases: str | Sequence[str] | None = None,
        store_name: str | None = None,
        action: Action[Option[T]] | None = None,
        num_args: int | numargs.BaseNumArgs | None = None,
        present: T | None = None,
        default: T | None = None,
        type_converter: Callable[[str], T] | None = None,
        choices: Sequence[T] | None = None,
        required: bool = False,
    ) -> Option[T]:
        long_names = (long_names,) if isinstance(long_names, str) else tuple(long_names or ())
        long_aliases = (
            (long_aliases,) if isinstance(long_aliases, str) else tuple(long_aliases or ())
        )

        short_names = (short_names,) if isinstance(short_names, str) else tuple(short_aliases or ())
        short_aliases = (
            (short_aliases,) if isinstance(short_aliases, str) else tuple(short_aliases or ())
        )

        if not long_names and not short_names:
            exc_message = "Either long_names or short_names must be a non-empty sequence"
            raise ValueError(exc_message)

        for short_name in short_names:
            if len(short_name) > 1:
                exc_message = f"short name {short_name!r} must have length 1, got {len(short_name)}"
                raise ValueError(exc_message)

        if store_name is None:
            store_name = long_names[0] if long_names else short_names[0]

        if action is None:
            action = store_value_action

        if num_args is None:
            if action in (
                store_present_action,
                store_true_action,
                store_false_action,
                append_present_action,
                count_presence_action,
            ):
                num_args = 0
            else:
                num_args = 1

        if action in (store_present_action, append_present_action) and present is None:
            action_name = getattr(action, "__name__", repr(action))
            exc_message = f"Missing present argument for action {action_name!r}"
            raise ValueError(exc_message)

        if present is not None and num_args != numargs.OPTIONAL:
            exc_message = (
                f"present argument must be used with num args {numargs.OPTIONAL!r}, "
                f"got {num_args!r}"
            )
            raise ValueError(exc_message)

        return cls(
            long_names=long_names,
            short_names=short_names,
            long_aliases=long_aliases,
            short_aliases=short_aliases,
            store_name=store_name,
            action=action,
            num_args=num_args,
            present=present,
            default=default,
            type_converter=type_converter or str,
            choices=tuple(choices or ()),
            required=required,
        )

    def __str__(self) -> str:
        return (
            long_specifiers[0]
            if (long_specifiers := self.long_specifiers)
            else self.short_specifiers[0]
        )

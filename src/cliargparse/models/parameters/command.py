from __future__ import annotations

from pathlib import Path
import sys
from typing import TYPE_CHECKING, Any

from cliargparse.enums import NArgs, ParseMode
from cliargparse.exceptions import (
    DuplicateOptionSpecifierError,
    DuplicatePositionalNameError,
    DuplicateSubcommandNameError,
    ParseModeError,
    PositionalAfterVariadicPositionalError,
)


if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Sequence

    from cliargparse.hints import Action
    from cliargparse.models.mutex_option_group import MutexOptionGroup

from cliargparse.models.namespace import Namespace

from .option import Option
from .parameter import Parameter
from .positional import Positional


class Command(Parameter):
    def __init__(
        self,
        name: str | None = None,
        *,
        aliases: str | Sequence[str] | None = None,
        parse_mode: ParseMode | None = None,
        subcommand_required: bool = False,
    ) -> None:
        self.name = name or Path(sys.argv[0]).name
        self.aliases: Sequence[str] = (
            (aliases,) if isinstance(aliases, str) else tuple(aliases or ())
        )
        self.parse_mode = parse_mode or ParseMode.COMMAND
        self.subcommand_required = subcommand_required

        self._options: list[Option[Any]] = []
        self._long_name_to_option: dict[str, Option[Any]] = {}
        self._short_name_to_option: dict[str, Option[Any]] = {}
        self._specifier_to_option: dict[str, Option[Any]] = {}

        self._mutex_option_groups: list[MutexOptionGroup] = []

        self._subcommands: list[Command] = []
        self._name_to_subcommand: dict[str, Command] = {}

        self._positionals: list[Positional[Any]] = []
        self._name_to_positional: dict[str, Positional[Any]] = {}

        self._variadic_positional: Positional[Any] | None = None

    @property
    def names(self) -> tuple[str, ...]:
        return (self.name, *self.aliases)

    @property
    def options(self) -> tuple[Option[Any], ...]:
        mutex_group_options = (
            option for group in self._mutex_option_groups for option in group.options
        )

        return (*self._options, *mutex_group_options)

    @property
    def variadic_options(self) -> tuple[Option[Any], ...]:
        return tuple(
            option
            for option in self.options
            if isinstance(option.nargs, NArgs) and option.nargs.is_variadic
        )

    @property
    def mutex_option_groups(self) -> tuple[MutexOptionGroup, ...]:
        return tuple(self._mutex_option_groups)

    @property
    def subcommands(self) -> tuple[Command, ...]:
        return tuple(self._subcommands)

    @property
    def positionals(self) -> tuple[Positional[Any], ...]:
        return tuple(self._positionals)

    @property
    def variadic_positional(self) -> Positional[Any] | None:
        return self._variadic_positional

    def add_option(self, option: Option[Any]) -> None:
        for specifier in option.specifiers:
            if existing_option := self._specifier_to_option.get(specifier):
                raise DuplicateOptionSpecifierError(specifier, existing_option, option)

        self._long_name_to_option.update(dict.fromkeys(option.long_names, option))
        self._short_name_to_option.update(dict.fromkeys(option.short_names, option))
        self._specifier_to_option.update(dict.fromkeys(option.specifiers, option))

        self._options.append(option)

    def option[T](
        self,
        long_names: str | Sequence[str] | None = None,
        short_names: str | Sequence[str] | None = None,
        *,
        long_aliases: str | Sequence[str] | None = None,
        short_aliases: str | Sequence[str] | None = None,
        store_name: str | None = None,
        action: Action[Option[T]] | None = None,
        nargs: int | NArgs | None = None,
        present: Any | None = None,
        default: Any | None = None,
        type_converter: Callable[[str], T] | None = None,
        choices: Sequence[T] | None = None,
        required: bool = False,
    ) -> Option[T]:
        option = Option[T].create(
            long_names=long_names,
            short_names=short_names,
            long_aliases=long_aliases,
            short_aliases=short_aliases,
            store_name=store_name,
            action=action,
            nargs=nargs,
            present=present,
            default=default,
            type_converter=type_converter,
            choices=choices,
            required=required,
        )
        self.add_option(option)

        return option

    def get_long_option(self, name: str, /) -> Option[Any] | None:
        return self._long_name_to_option.get(name)

    def get_short_option(self, name: str, /) -> Option[Any] | None:
        return self._short_name_to_option.get(name)

    def get_option(self, specifier: str, /) -> Option[Any] | None:
        return self._specifier_to_option.get(specifier)

    def has_option(self, option: str | Option[Any], /) -> bool:
        if isinstance(option, str):
            return option in self._specifier_to_option

        return option in self._options

    def remove_option(self, key: str | Option[Any], /) -> Option[Any]:
        if isinstance(key, str):
            option = self.get_option(key)
            if not option:
                exc_message = f"Option with specifier {key!r} not found"
                raise ValueError(exc_message)
        else:
            option = key

        try:
            self._options.remove(option)
        except ValueError:
            exc_message = f"Option not found: {option}"
            raise ValueError(exc_message) from None

        for specifier in option.specifiers:
            del self._specifier_to_option[specifier]

        return option

    def mutex_option_group(self, *, required: bool = False) -> MutexOptionGroup:
        from cliargparse.models.mutex_option_group import MutexOptionGroup  # noqa: PLC0415

        group = MutexOptionGroup(self, required)
        self._mutex_option_groups.append(group)

        return group

    def add_subcommand(self, subcommand: Command, /) -> None:
        if self.parse_mode != ParseMode.COMMAND:
            exc_message = f"Subcommands are not allowed in {self.parse_mode.name} parse mode"
            raise ParseModeError(exc_message)

        for name in subcommand.names:
            if existing_subcommand := self._name_to_subcommand.get(name):
                raise DuplicateSubcommandNameError(name, existing_subcommand, subcommand)

        self._name_to_subcommand.update(dict.fromkeys(subcommand.names, subcommand))
        self._subcommands.append(subcommand)

    def subcommand(
        self,
        name: str,
        *,
        parse_mode: ParseMode | None = None,
        subcommand_required: bool = False,
    ) -> Command:
        subcommand = Command(
            name=name,
            parse_mode=parse_mode,
            subcommand_required=subcommand_required,
        )
        self.add_subcommand(subcommand)

        return subcommand

    def get_subcommand(self, name: str, /) -> Command | None:
        return self._name_to_subcommand.get(name)

    def add_positional(self, positional: Positional[Any], /) -> None:
        if self.parse_mode != ParseMode.POSITIONAL:
            exc_message = f"Positionals are not allowed in {self.parse_mode.name} parse mode"
            raise ParseModeError(exc_message)

        if existing_positional := self._name_to_positional.get(positional.name):
            raise DuplicatePositionalNameError(positional.name, existing_positional, positional)

        if self.variadic_positional:
            raise PositionalAfterVariadicPositionalError(self.variadic_positional)

        if isinstance(positional.nargs, NArgs) and positional.nargs.is_variadic:
            self._variadic_positional = positional

        self._name_to_positional[positional.name] = positional
        self._positionals.append(positional)

    def positional[T](
        self,
        name: str,
        *,
        action: Action[Positional[T]] | None = None,
        nargs: int | NArgs | None = None,
        default: Any | None = None,
        type_converter: Callable[[str], T] | None = None,
        choices: Sequence[T] | None = None,
    ) -> Positional[T]:
        positional = Positional[T].create(
            name=name,
            action=action,
            nargs=nargs,
            default=default,
            type_converter=type_converter,
            choices=choices,
        )
        self.add_positional(positional)

        return positional

    def get_positional(self, name: str, /) -> Positional[Any] | None:
        return self._name_to_positional.get(name)

    def get_positional_by_index(self, index: int, /) -> Positional[Any]:
        return self._positionals[index]

    def parse_input(self, data: str | Iterable[str], /) -> Namespace:
        from cliargparse.lexer import lex  # noqa: PLC0415
        from cliargparse.parser import parse  # noqa: PLC0415

        lexemes: Iterable[str]
        if isinstance(data, str):
            import shlex  # noqa: PLC0415

            lexemes = shlex.split(data)
        else:
            lexemes = data

        tokens = lex(lexemes)

        node = parse(tokens, self)
        return Namespace.from_node(node)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"name={self.name!r}, "
            f"aliases={self.aliases}, "
            f"parse_mode={self.parse_mode!r}, "
            f"subcommand_required={self.subcommand_required}, "
            f"options={self.options}, "
            f"variadic_options={self.variadic_options}, "
            f"mutex_option_groups={self.mutex_option_groups}, "
            f"subcommands={self.subcommands}, "
            f"positionals={self.positionals}, "
            f"variadic_positional={self.variadic_positional}"
            ")"
        )

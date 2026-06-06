from __future__ import annotations

from pathlib import Path
import sys
from typing import TYPE_CHECKING, Any, override

from clargparse import numargs
from clargparse.enums import ParseMode
from clargparse.exceptions import ParseModeError


if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Sequence

    from clargparse.models.mutex_option_group import MutexOptionGroup
    from clargparse.typing import Action

from clargparse.models.parsed_command_input import ParsedCommandInput
from clargparse.tokenizer import tokenize
from clargparse.tokenizer.tokens import TokenizerToken

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

        self._subcommands: list[Command] = []
        self._name_to_subcommand: dict[str, Command] = {}

        self._options: list[Option[Any]] = []
        self._long_name_to_option: dict[str, Option[Any]] = {}
        self._short_name_to_option: dict[str, Option[Any]] = {}
        self._specifier_to_option: dict[str, Option[Any]] = {}

        self._mutex_option_groups: list[MutexOptionGroup] = []

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
            if isinstance(option.num_args, numargs.BaseNumArgs) and option.num_args.is_variadic
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

    def add_subcommand(self, subcommand: Command, /) -> None:
        if self.parse_mode != ParseMode.COMMAND:
            exc_message = f"Subcommands are not allowed in {self.parse_mode.name} parse mode"
            raise ParseModeError(exc_message)

        for name in subcommand.names:
            if name in self._name_to_subcommand:
                exc_message = f"command {name!r} already exists"
                raise ValueError(exc_message)

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

    def has_subcommand(self, key: str | Command, /) -> bool:
        if isinstance(key, str):
            return key in self._name_to_subcommand

        return key in self._subcommands

    def get_subcommand(self, name: str, /) -> Command | None:
        return self._name_to_subcommand.get(name)

    def remove_subcommand(self, key: str | Command, /) -> Command:
        if isinstance(key, str):
            subcommand = self.get_subcommand(key)
            if not subcommand:
                exc_message = f"subcommand {key!r} not found"
                raise ValueError(exc_message)
        else:
            subcommand = key

        try:
            self._subcommands.remove(subcommand)
        except ValueError:
            exc_message = f"subcommand not found: {subcommand}"
            raise ValueError(exc_message) from None

        for name in subcommand.names:
            del self._name_to_subcommand[name]

        return subcommand

    def add_option(self, option: Option[Any]) -> None:
        for specifier in option.specifiers:
            if specifier in self._specifier_to_option:
                exc_message = f"option {specifier!r} already exists"
                raise ValueError(exc_message)

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
        num_args: int | numargs.BaseNumArgs | None = None,
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
            num_args=num_args,
            present=present,
            default=default,
            type_converter=type_converter,
            choices=choices,
            required=required,
        )
        self.add_option(option)

        return option

    def has_option(self, key: str | Option[Any], /) -> bool:
        if isinstance(key, str):
            return key in self._specifier_to_option

        return key in self._options

    def get_long_option(self, name: str, /) -> Option[Any] | None:
        return self._long_name_to_option.get(name)

    def get_short_option(self, name: str, /) -> Option[Any] | None:
        return self._short_name_to_option.get(name)

    def get_option(self, specifier: str, /) -> Option[Any] | None:
        return self._specifier_to_option.get(specifier)

    def remove_option(self, key: str | Option[Any], /) -> Option[Any]:
        if isinstance(key, str):
            option = self.get_option(key)
            if not option:
                exc_message = f"option with specifier {key!r} not found"
                raise ValueError(exc_message)
        else:
            option = key

        try:
            self._options.remove(option)
        except ValueError:
            exc_message = f"option not found: {option}"
            raise ValueError(exc_message) from None

        for specifier in option.specifiers:
            del self._specifier_to_option[specifier]

        return option

    def mutex_option_group(self, *, required: bool = False) -> MutexOptionGroup:
        from clargparse.models.mutex_option_group import MutexOptionGroup  # noqa: PLC0415

        group = MutexOptionGroup(self, required)
        self._mutex_option_groups.append(group)

        return group

    def has_mutex_option_group(self, group: MutexOptionGroup, /) -> bool:
        return group in self._mutex_option_groups

    def remove_mutex_option_group(self, group: MutexOptionGroup, /) -> None:
        if group not in self._mutex_option_groups:
            exc_message = f"Mutex option group not found: {group}"
            raise ValueError(exc_message)

        for option in group:
            self.remove_option(option)

        self._mutex_option_groups.remove(group)

    def add_positional(self, positional: Positional[Any], /) -> None:
        if self.parse_mode != ParseMode.POSITIONAL:
            exc_message = f"positionals are not allowed in {self.parse_mode.name} parse mode"
            raise ParseModeError(exc_message)

        if positional.name in self._name_to_positional:
            exc_message = f"positional {self.name!r} already exists"
            raise ValueError(exc_message)

        if self._variadic_positional:
            exc_message = (
                "cannot add positional "
                f"after variadic positional {self._variadic_positional.name!r}"
            )
            raise ValueError(exc_message)

        if (
            positional.default is None
            and self._positionals
            and self._positionals[-1].default is not None
        ):
            exc_message = (
                "positional without default argument cannot follow positional with default argument"
            )
            raise ValueError(exc_message)

        if isinstance(positional.num_args, numargs.BaseNumArgs) and positional.num_args.is_variadic:
            self._variadic_positional = positional

        self._name_to_positional[positional.name] = positional
        self._positionals.append(positional)

    def positional[T](
        self,
        name: str,
        *,
        action: Action[Positional[T]] | None = None,
        num_args: int | numargs.BaseNumArgs | None = None,
        default: Any | None = None,
        type_converter: Callable[[str], T] | None = None,
        choices: Sequence[T] | None = None,
    ) -> Positional[T]:
        positional = Positional[T].create(
            name=name,
            action=action,
            num_args=num_args,
            default=default,
            type_converter=type_converter,
            choices=choices,
        )
        self.add_positional(positional)

        return positional

    def has_positional(self, key: str | Positional[Any], /) -> bool:
        if isinstance(key, str):
            return key in self._name_to_positional

        return key in self._positionals

    def get_positional(self, name: str, /) -> Positional[Any] | None:
        return self._name_to_positional.get(name)

    def get_positional_by_index(self, index: int, /) -> Positional[Any] | None:
        try:
            return self._positionals[index]
        except IndexError:
            return None

    def remove_positional(self, key: str | Positional[Any], /) -> Positional[Any]:
        if isinstance(key, str):
            positional = self.get_positional(key)
            if not positional:
                exc_message = f"positional {key!r} not found"
                raise ValueError(exc_message)
        else:
            positional = key

        try:
            self._positionals.remove(positional)
        except ValueError:
            exc_message = f"positional not found: {positional}"
            raise ValueError(exc_message) from None

        return positional

    def parse_input(self, data: str | Iterable[str], /) -> ParsedCommandInput:
        tokenizer_tokens: list[TokenizerToken]
        if isinstance(data, str):
            tokenizer_tokens = tokenize(data)
        else:
            tokenizer_tokens = [TokenizerToken(value) for value in data]

        return self.parse_tokenizer_tokens(tokenizer_tokens)

    def parse_tokenizer_tokens(self, tokens: Iterable[TokenizerToken], /) -> ParsedCommandInput:
        from clargparse.lexer import lex  # noqa: PLC0415
        from clargparse.parser import parse  # noqa: PLC0415

        lexer_tokens = lex(tokens)
        node = parse(lexer_tokens, self)
        return ParsedCommandInput.from_node(node)

    @override
    def __str__(self) -> str:
        return self.name

    @override
    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"name={self.name!r}, "
            f"aliases={self.aliases}, "
            f"parse_mode={self.parse_mode!r}, "
            f"subcommand_required={self.subcommand_required}, "
            f"options={self._options}, "
            f"variadic_options={self.variadic_options}, "
            f"mutex_option_groups={self._mutex_option_groups}, "
            f"subcommands={self._subcommands}, "
            f"positionals={self._positionals}, "
            f"variadic_positional={self._variadic_positional}"
            ")"
        )

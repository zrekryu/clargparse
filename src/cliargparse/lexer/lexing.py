from __future__ import annotations

from typing import TYPE_CHECKING, Final

from cliargparse.enums import OptionPrefix
from cliargparse.exceptions import MissingOptionNameError, ShortOptionNameTooLongError

from .tokens import ArgumentToken, OptionToken, ShortOptionGroupToken


if TYPE_CHECKING:
    from collections.abc import Generator, Iterable

    from cliargparse.hints import LexerToken


END_OF_OPTIONS: Final[str] = "--"
OPTION_VALUE_DELIMITER: Final[str] = "="


def lex(arguments: Iterable[str]) -> Generator[LexerToken]:
    end_of_options = False

    for argument in arguments:
        if not end_of_options:
            if argument == END_OF_OPTIONS:
                end_of_options = True
            elif argument == OptionPrefix.SHORT:
                yield ArgumentToken(argument)
            elif argument.startswith(OptionPrefix.LONG):
                yield _lex_long_option_prefix(argument)
            elif argument.startswith(OptionPrefix.SHORT):
                _lex_short_option_prefix(argument)
        else:
            yield ArgumentToken(argument)


def _lex_long_option_prefix(argument: str) -> OptionToken | ArgumentToken:
    prefix_len = len(OptionPrefix.LONG)
    first_char = argument[prefix_len : prefix_len + 1]

    if first_char.isalpha():
        return _lex_long_option(argument)
    if first_char.isdigit():
        return ArgumentToken(argument)

    exc_message = f"unreachable code reached: {argument}"
    raise AssertionError(exc_message)


def _lex_short_option_prefix(argument: str) -> OptionToken | ShortOptionGroupToken | ArgumentToken:
    prefix_len = len(OptionPrefix.SHORT)
    first_char = argument[prefix_len : prefix_len + 1]

    if first_char.isalpha():
        return _lex_short_option_or_group(argument)
    if first_char.isdigit():
        return ArgumentToken(argument)

    exc_message = f"unreachable code reached: {argument}"
    raise AssertionError(exc_message)


def _lex_long_option(argument: str) -> OptionToken:
    value: str | None
    name, sep, value = argument.removeprefix(OptionPrefix.LONG).partition(
        OPTION_VALUE_DELIMITER,
    )

    if not name:
        raise MissingOptionNameError(argument)

    if not sep:
        value = None

    return OptionToken(
        argument=argument,
        prefix=OptionPrefix.LONG,
        name=name,
        value=value,
    )


def _lex_short_option_or_group(argument: str) -> OptionToken | ShortOptionGroupToken:
    unprefixed_argument = argument.removeprefix(OptionPrefix.SHORT)
    if len(unprefixed_argument) > 1 and unprefixed_argument[1] != OPTION_VALUE_DELIMITER:
        return ShortOptionGroupToken(
            argument,
            tuple(OptionToken(name, OptionPrefix.SHORT, name) for name in unprefixed_argument),
        )

    return _build_short_option(argument, unprefixed_argument)


def _build_short_option(argument: str, unprefixed_argument: str) -> OptionToken:
    value: str | None
    name, sep, value = unprefixed_argument.partition(OPTION_VALUE_DELIMITER)

    if len(name) > 1:
        raise ShortOptionNameTooLongError(name)

    if not sep:
        value = None

    return OptionToken(
        argument=argument,
        prefix=OptionPrefix.SHORT,
        name=name,
        value=value,
    )

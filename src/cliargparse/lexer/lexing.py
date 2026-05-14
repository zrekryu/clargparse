from collections.abc import Generator, Iterable
from typing import Final

from cliargparse.enums import OptionPrefix
from cliargparse.exceptions import MissingOptionNameError, ShortOptionNameTooLongError
from cliargparse.hints import LexerToken

from .tokens import ArgumentToken, OptionToken, ShortOptionGroupToken


END_OF_OPTIONS: Final[str] = "--"
OPTION_VALUE_DELIMITER: Final[str] = "="


def lex(arguments: Iterable[str]) -> Generator[LexerToken]:
    end_of_options = False

    for argument in arguments:
        if argument.startswith(OptionPrefix.LONG):
            if argument[len(OptionPrefix.LONG) :].isdigit():
                yield ArgumentToken(argument)
                continue
            elif not end_of_options:
                if argument == END_OF_OPTIONS:
                    end_of_options = True
                    continue

                yield _lex_long_option(argument)
                continue
        elif argument.startswith(OptionPrefix.SHORT):
            if argument == OptionPrefix.SHORT or argument[len(OptionPrefix.SHORT) :].isdigit():
                yield ArgumentToken(argument)
                continue
            elif not end_of_options:
                yield _lex_short_option_or_group(argument)
                continue

        yield ArgumentToken(argument)


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

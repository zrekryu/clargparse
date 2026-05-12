from collections.abc import Generator, Iterable
from typing import Final

from cliargparse.enums import OptionPrefix
from cliargparse.exceptions import MissingOptionNameError, ShortOptionNameTooLongError
from cliargparse.hints import LexerToken

from .tokens import ArgumentToken, OptionToken, ShortOptionGroupToken


END_OF_OPTIONS: Final[str] = "--"
OPTION_ARGUMENT_DELIMITER: Final[str] = "="


def lex(lexemes: Iterable[str]) -> Generator[LexerToken]:
    end_of_options = False

    for lexeme in lexemes:
        if lexeme.startswith(OptionPrefix.LONG):
            if lexeme[len(OptionPrefix.LONG) :].isdigit():
                yield ArgumentToken(lexeme)
                continue
            elif not end_of_options:
                if lexeme == END_OF_OPTIONS:
                    end_of_options = True
                    continue

                yield _lex_long_option(lexeme)
                continue
        elif lexeme.startswith(OptionPrefix.SHORT):
            if lexeme == OptionPrefix.SHORT or lexeme[len(OptionPrefix.SHORT) :].isdigit():
                yield ArgumentToken(lexeme)
                continue
            elif not end_of_options:
                yield _lex_short_option_or_group(lexeme)
                continue

        yield ArgumentToken(lexeme)


def _lex_long_option(lexeme: str) -> OptionToken:
    argument: str | None
    name, sep, argument = lexeme.removeprefix(OptionPrefix.LONG).partition(
        OPTION_ARGUMENT_DELIMITER,
    )

    if not name:
        raise MissingOptionNameError(lexeme)

    if not sep:
        argument = None

    return OptionToken(
        lexeme=lexeme,
        prefix=OptionPrefix.LONG,
        name=name,
        argument=argument,
    )


def _lex_short_option_or_group(lexeme: str) -> OptionToken | ShortOptionGroupToken:
    unprefixed_lexeme = lexeme.removeprefix(OptionPrefix.SHORT)
    if len(unprefixed_lexeme) > 1 and unprefixed_lexeme[1] != OPTION_ARGUMENT_DELIMITER:
        return ShortOptionGroupToken(
            lexeme,
            tuple(OptionToken(name, OptionPrefix.SHORT, name) for name in unprefixed_lexeme),
        )

    return _build_short_option(lexeme, unprefixed_lexeme)


def _build_short_option(lexeme: str, unprefixed_lexeme: str) -> OptionToken:
    argument: str | None
    name, sep, argument = unprefixed_lexeme.partition(OPTION_ARGUMENT_DELIMITER)

    if len(name) != 1:
        raise ShortOptionNameTooLongError(name)

    if not sep:
        argument = None

    return OptionToken(
        lexeme=lexeme,
        prefix=OptionPrefix.SHORT,
        name=name,
        argument=argument,
    )

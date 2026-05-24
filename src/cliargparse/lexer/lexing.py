from __future__ import annotations

from typing import TYPE_CHECKING, Final

from cliargparse.enums import OptionPrefix
from cliargparse.exceptions import MissingOptionNameError, ShortOptionNameTooLongError

from .tokens import ArgumentToken, OptionToken, ShortOptionGroupToken


if TYPE_CHECKING:
    from collections.abc import Generator, Iterable

    from cliargparse.hints import LexerTokenUnion
    from cliargparse.tokenizer.tokens import TokenizerToken


END_OF_OPTIONS: Final[str] = "--"
OPTION_VALUE_DELIMITER: Final[str] = "="


def lex(tokens: Iterable[TokenizerToken]) -> Generator[LexerTokenUnion]:
    end_of_options = False

    for token in tokens:
        argument = token.argument
        if not end_of_options:
            if argument == END_OF_OPTIONS:
                end_of_options = True
            elif argument == OptionPrefix.SHORT:
                yield ArgumentToken(token)
            elif argument.startswith(OptionPrefix.LONG):
                yield _lex_long_option_prefix(token)
            elif argument.startswith(OptionPrefix.SHORT):
                _lex_short_option_prefix(token)
        else:
            yield ArgumentToken(token)


def _lex_long_option_prefix(token: TokenizerToken) -> OptionToken | ArgumentToken:
    prefix_len = len(OptionPrefix.LONG)
    first_char = token.argument[prefix_len : prefix_len + 1]

    if first_char.isalpha():
        return _lex_long_option(token)
    if first_char.isdigit():
        return ArgumentToken(token)

    exc_message = f"unreachable code reached: {token}"
    raise AssertionError(exc_message)


def _lex_short_option_prefix(
    token: TokenizerToken,
) -> OptionToken | ShortOptionGroupToken | ArgumentToken:
    prefix_len = len(OptionPrefix.SHORT)
    first_char = token.argument[prefix_len : prefix_len + 1]

    if first_char.isalpha():
        return _lex_short_option_or_group(token)
    if first_char.isdigit():
        return ArgumentToken(token)

    exc_message = f"unreachable code reached: {token}"
    raise AssertionError(exc_message)


def _lex_long_option(token: TokenizerToken) -> OptionToken:
    value: str | None
    name, sep, value = token.argument.removeprefix(OptionPrefix.LONG).partition(
        OPTION_VALUE_DELIMITER,
    )

    if not name:
        raise MissingOptionNameError(token.argument)

    if not sep:
        value = None

    return OptionToken(
        token=token,
        prefix=OptionPrefix.LONG,
        name=name,
        value=value,
    )


def _lex_short_option_or_group(token: TokenizerToken) -> OptionToken | ShortOptionGroupToken:
    unprefixed_argument = token.argument.removeprefix(OptionPrefix.SHORT)
    if len(unprefixed_argument) > 1 and unprefixed_argument[1] != OPTION_VALUE_DELIMITER:
        return ShortOptionGroupToken(
            token,
            tuple(OptionToken(token, OptionPrefix.SHORT, name) for name in unprefixed_argument),
        )

    return _build_short_option(token, unprefixed_argument)


def _build_short_option(token: TokenizerToken, unprefixed_argument: str) -> OptionToken:
    value: str | None
    name, sep, value = unprefixed_argument.partition(OPTION_VALUE_DELIMITER)

    if len(name) > 1:
        raise ShortOptionNameTooLongError(name)

    if not sep:
        value = None

    return OptionToken(
        token=token,
        prefix=OptionPrefix.SHORT,
        name=name,
        value=value,
    )

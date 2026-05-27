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
OPTION_ARGUMENT_DELIMITER: Final[str] = "="


def lex(tokens: Iterable[TokenizerToken]) -> Generator[LexerTokenUnion]:
    end_of_options = False

    for token in tokens:
        value = token.value
        if not end_of_options:
            if value == END_OF_OPTIONS:
                end_of_options = True
            elif value == OptionPrefix.SHORT:
                yield ArgumentToken(token)
            elif value.startswith(OptionPrefix.LONG):
                yield _lex_long_option_prefix(token)
            elif value.startswith(OptionPrefix.SHORT):
                yield _lex_short_option_prefix(token)
        else:
            yield ArgumentToken(token)


def _lex_long_option_prefix(token: TokenizerToken) -> OptionToken | ArgumentToken:
    prefix_len = len(OptionPrefix.LONG)
    first_char = token.value[prefix_len : prefix_len + 1]

    if first_char.isdigit():
        return ArgumentToken(token)

    return _lex_long_option(token)


def _lex_short_option_prefix(
    token: TokenizerToken,
) -> OptionToken | ShortOptionGroupToken | ArgumentToken:
    prefix_len = len(OptionPrefix.SHORT)
    first_char = token.value[prefix_len : prefix_len + 1]

    if first_char.isdigit():
        return ArgumentToken(token)

    return _lex_short_option_or_group(token)


def _lex_long_option(token: TokenizerToken) -> OptionToken:
    argument: str | None
    name, sep, argument = token.value.removeprefix(OptionPrefix.LONG).partition(
        OPTION_ARGUMENT_DELIMITER,
    )

    if not name:
        raise MissingOptionNameError(token.value)

    if not sep:
        argument = None

    return OptionToken(
        token=token,
        prefix=OptionPrefix.LONG,
        name=name,
        argument=argument,
    )


def _lex_short_option_or_group(token: TokenizerToken) -> OptionToken | ShortOptionGroupToken:
    unprefixed_argument = token.value.removeprefix(OptionPrefix.SHORT)
    if len(unprefixed_argument) > 1 and unprefixed_argument[1] != OPTION_ARGUMENT_DELIMITER:
        return ShortOptionGroupToken(
            token,
            tuple(OptionToken(token, OptionPrefix.SHORT, name) for name in unprefixed_argument),
        )

    return _build_short_option(token, unprefixed_argument)


def _build_short_option(token: TokenizerToken, unprefixed_argument: str) -> OptionToken:
    argument: str | None
    name, sep, argument = unprefixed_argument.partition(OPTION_ARGUMENT_DELIMITER)

    if len(name) > 1:
        raise ShortOptionNameTooLongError(name)

    if not sep:
        argument = None

    return OptionToken(
        token=token,
        prefix=OptionPrefix.SHORT,
        name=name,
        argument=argument,
    )

from __future__ import annotations

from typing import Final, assert_never

from cliargparse.enums import TokenizerState
from cliargparse.exceptions import (
    InvalidEscapeSequenceError,
    UnclosedQuoteError,
    UnterminatedEscapeSequenceError,
)

from .tokenize_context import TokenizeContext
from .tokens import TokenizerToken


SINGLE_QUOTE: Final = "'"
DOUBLE_QUOTE: Final = '"'
QUOTES: Final = SINGLE_QUOTE + DOUBLE_QUOTE

BACKSLASH: Final = "\\"


def tokenize(source: str) -> list[TokenizerToken]:
    context = TokenizeContext(source)

    while context.source_index < len(context.source):
        if not context.buffer:
            context.argument_start_index = context.source_index

        char = source[context.source_index]

        match context.state:
            case TokenizerState.UNQUOTED:
                _handle_unquoted(char, context)
            case TokenizerState.SINGLE_QUOTE:
                _handle_single_quote(char, context)
            case TokenizerState.DOUBLE_QUOTE:
                _handle_double_quote(char, context)
            case _:
                assert_never(context.state)

    if context.state != TokenizerState.UNQUOTED:
        match context.state:
            case TokenizerState.SINGLE_QUOTE:
                raise UnclosedQuoteError(SINGLE_QUOTE, context.state_start_index)
            case TokenizerState.DOUBLE_QUOTE:
                raise UnclosedQuoteError(DOUBLE_QUOTE, context.state_start_index)
            case _:
                assert_never(context.state)

    if context.buffer:
        context.argument_end_index = context.source_index
        _flush_buffer(context)

    return context.tokens


def _flush_buffer(context: TokenizeContext) -> None:
    value = "".join(context.buffer)

    token = TokenizerToken(
        value, start_index=context.argument_start_index, end_index=context.argument_end_index
    )
    context.tokens.append(token)

    context.buffer.clear()


def _handle_unquoted(char: str, context: TokenizeContext) -> None:
    if char == SINGLE_QUOTE:
        context.state_start_index = context.source_index
        context.state = TokenizerState.SINGLE_QUOTE
        context.source_index += 1
    elif char == DOUBLE_QUOTE:
        context.state_start_index = context.source_index
        context.state = TokenizerState.DOUBLE_QUOTE
        context.source_index += 1
    elif char.isspace():
        if context.buffer:
            context.argument_end_index = context.source_index
            _flush_buffer(context)

        context.source_index += 1
    elif char == BACKSLASH:
        next_char = _peak_source_char(context.source, context.source_index)
        if not next_char:
            raise UnterminatedEscapeSequenceError(context.source_index)

        if next_char in QUOTES or next_char == BACKSLASH:
            context.buffer.append(next_char)
            context.source_index += 2
        else:
            raise InvalidEscapeSequenceError(next_char, context.source_index)
    else:
        context.buffer.append(char)
        context.source_index += 1


def _handle_single_quote(char: str, context: TokenizeContext) -> None:
    if char == SINGLE_QUOTE:
        context.state_start_index = context.source_index
        context.state = TokenizerState.UNQUOTED
        context.source_index += 1
    else:
        context.buffer.append(char)
        context.source_index += 1


def _handle_double_quote(char: str, context: TokenizeContext) -> None:
    if char == DOUBLE_QUOTE:
        context.state_start_index = context.source_index
        context.state = TokenizerState.UNQUOTED
        context.source_index += 1
    elif char == BACKSLASH:
        next_char = _peak_source_char(context.source, context.source_index)
        if not next_char:
            raise UnterminatedEscapeSequenceError(context.source_index)

        if next_char in QUOTES or next_char == BACKSLASH:
            context.buffer.append(next_char)
            context.source_index += 2
        else:
            raise InvalidEscapeSequenceError(next_char, context.source_index)
    else:
        context.buffer.append(char)
        context.source_index += 1


def _peak_source_char(source: str, source_index: int) -> str | None:
    if source_index + 1 < len(source):
        return source[source_index + 1]

    return None

from __future__ import annotations

from typing import Final, assert_never

from clargparse.enums import TokenizerState
from clargparse.exceptions import (
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

    _flush_buffer(context)

    return context.tokens


def _flush_buffer(context: TokenizeContext) -> None:
    if not context.buffer:
        return

    if context.last_buffered_index is None:
        exc_message = (
            f"context.last_buffered_index must not be None, got {context.last_buffered_index}"
        )
        raise RuntimeError(exc_message)

    value = "".join(context.buffer)

    token = TokenizerToken(
        value, start_index=context.token_start_index, end_index=context.last_buffered_index + 1
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
        _flush_buffer(context)
        context.source_index += 1
    elif char == BACKSLASH:
        next_char = _peek_source_char(context.source, context.source_index)
        if not next_char:
            raise UnterminatedEscapeSequenceError(context.source_index)

        if next_char in QUOTES or next_char == BACKSLASH or next_char.isspace():
            context.buffer.append(next_char)
            context.last_buffered_index = context.source_index + 1
            context.source_index += 2

        else:
            raise InvalidEscapeSequenceError(next_char, context.source_index)
    else:
        if not context.buffer:
            context.token_start_index = context.source_index

        context.buffer.append(char)
        context.last_buffered_index = context.source_index
        context.source_index += 1


def _handle_single_quote(char: str, context: TokenizeContext) -> None:
    if char == SINGLE_QUOTE:
        context.state_start_index = context.source_index
        context.state = TokenizerState.UNQUOTED
        context.source_index += 1
    else:
        if not context.buffer:
            context.token_start_index = context.source_index

        context.buffer.append(char)
        context.last_buffered_index = context.source_index
        context.source_index += 1


def _handle_double_quote(char: str, context: TokenizeContext) -> None:
    if char == DOUBLE_QUOTE:
        context.state_start_index = context.source_index
        context.state = TokenizerState.UNQUOTED
        context.source_index += 1
    elif char == BACKSLASH:
        next_char = _peek_source_char(context.source, context.source_index)
        if not next_char:
            raise UnterminatedEscapeSequenceError(context.source_index)

        if next_char in QUOTES or next_char == BACKSLASH or next_char.isspace():
            context.buffer.append(next_char)
            context.last_buffered_index = context.source_index + 1
            context.source_index += 2
        else:
            raise InvalidEscapeSequenceError(next_char, context.source_index)
    else:
        if not context.buffer:
            context.token_start_index = context.source_index

        context.buffer.append(char)
        context.last_buffered_index = context.source_index
        context.source_index += 1


def _peek_source_char(source: str, source_index: int) -> str | None:
    if source_index + 1 < len(source):
        return source[source_index + 1]

    return None

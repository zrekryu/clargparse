from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from collections.abc import Iterable

    from cliargparse.hints import LexerTokenUnion


class TokenStream:
    def __init__(self, tokens: Iterable[LexerTokenUnion]) -> None:
        self._iter = iter(tokens)

        self._buffer: LexerTokenUnion | None = None

    def peek(self) -> LexerTokenUnion | None:
        if self._buffer is None:
            try:
                self._buffer = next(self._iter)
            except StopIteration:
                return None

        return self._buffer

    def consume(self) -> LexerTokenUnion | None:
        token = self.peek()
        self._buffer = None
        return token

    def __iter__(self) -> TokenStream:
        return self

    def __next__(self) -> LexerTokenUnion:
        token = self.peek()
        if token is None:
            raise StopIteration

        self._buffer = None

        return token

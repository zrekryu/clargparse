from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from collections.abc import Iterable

    from cliargparse.hints import LexerToken


class TokenStream:
    def __init__(self, tokens: Iterable[LexerToken]) -> None:
        self._iter = iter(tokens)

        self._buffer: LexerToken | None = None

    def peek(self) -> LexerToken | None:
        if self._buffer is None:
            try:
                self._buffer = next(self._iter)
            except StopIteration:
                return None

        return self._buffer

    def consume(self) -> LexerToken | None:
        token = self.peek()
        self._buffer = None
        return token

    def __iter__(self) -> TokenStream:
        return self

    def __next__(self) -> LexerToken:
        token = self.peek()
        if token is None:
            raise StopIteration

        self._buffer = None

        return token

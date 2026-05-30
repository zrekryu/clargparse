from __future__ import annotations

from typing import Literal, override

from .base import CLIError


class TokenizerError(CLIError):
    pass


class UnclosedQuoteError(TokenizerError):
    def __init__(self, quote: Literal["'", '"'], open_index: int) -> None:
        super().__init__(quote, open_index)

        self.quote = quote
        self.open_index = open_index

    @override
    def __str__(self) -> str:
        return f"unclosed {self.quote!r} quote opened at index {self.open_index}"


class InvalidEscapeSequenceError(TokenizerError):
    def __init__(self, char: str, index: int) -> None:
        super().__init__(char, index)

        self.char = char
        self.index = index

    @override
    def __str__(self) -> str:
        return f"invalid escape sequence '\\{self.char}' at index {self.index}"


class UnterminatedEscapeSequenceError(TokenizerError):
    def __init__(self, index: int) -> None:
        super().__init__(index)

        self.index = index

    @override
    def __str__(self) -> str:
        return f"unterminated escape sequence at end of source (index {self.index})"

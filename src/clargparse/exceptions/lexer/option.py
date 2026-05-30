from __future__ import annotations

from typing import override

from .base import LexerError


class MissingOptionNameError(LexerError):
    argument: str

    @override
    def __str__(self) -> str:
        return f"missing option name: {self.argument}"


class ShortOptionNameTooLongError(LexerError):
    name: str

    @override
    def __str__(self) -> str:
        return f"short option name {self.name} length must to be 1, got {len(self.name)}"

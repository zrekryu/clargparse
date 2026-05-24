from __future__ import annotations

from dataclasses import dataclass

from .token import LexerToken


@dataclass(frozen=True)
class ArgumentToken(LexerToken):
    pass

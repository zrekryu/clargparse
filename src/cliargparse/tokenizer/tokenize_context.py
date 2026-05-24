from __future__ import annotations

from dataclasses import dataclass, field

from cliargparse.enums import TokenizerState

from .tokens import TokenizerToken


@dataclass
class TokenizeContext:
    source: str
    source_index: int = 0

    state_start_index = 0
    state: TokenizerState = TokenizerState.UNQUOTED

    buffer: list[str] = field(default_factory=list[str])
    tokens: list[TokenizerToken] = field(default_factory=list[TokenizerToken])

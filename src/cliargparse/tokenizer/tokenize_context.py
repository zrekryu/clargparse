from __future__ import annotations

from dataclasses import KW_ONLY, dataclass, field

from cliargparse.enums import TokenizerState

from .tokens import TokenizerToken


@dataclass
class TokenizeContext:
    source: str

    _: KW_ONLY

    source_index: int = 0
    argument_start_index: int = 0
    argument_end_index: int = 0

    state_start_index = 0
    state: TokenizerState = TokenizerState.UNQUOTED

    buffer: list[str] = field(default_factory=list[str])
    tokens: list[TokenizerToken] = field(default_factory=list[TokenizerToken])

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from cliargparse.tokenizer.tokens import TokenizerToken


@dataclass(frozen=True)
class LexerToken:
    token: TokenizerToken

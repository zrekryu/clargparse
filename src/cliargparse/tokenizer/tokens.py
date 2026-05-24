from __future__ import annotations

from dataclasses import KW_ONLY, dataclass


@dataclass(frozen=True)
class TokenizerToken:
    argument: str

    _: KW_ONLY

    start_index: int | None = None

    def __str__(self) -> str:
        return self.argument

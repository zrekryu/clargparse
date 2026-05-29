from __future__ import annotations

from dataclasses import KW_ONLY, dataclass
from typing import override


@dataclass(frozen=True)
class TokenizerToken:
    value: str

    _: KW_ONLY

    start_index: int | None = None
    end_index: int | None = None

    @override
    def __str__(self) -> str:
        return self.value

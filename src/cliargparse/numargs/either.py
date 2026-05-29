from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, override

from .base import BaseNumArgs


@dataclass(frozen=True)
class Either(BaseNumArgs):
    MINIMUM_COUNT: ClassVar[int] = 2

    counts: tuple[int, ...]

    def __init__(self, *counts: int) -> None:
        if len(counts) < self.MINIMUM_COUNT:
            exc_message = f"Either must receive at least 2 counts, got {len(counts)}"
            raise ValueError(exc_message)

        object.__setattr__(self, "counts", tuple(sorted(counts)))

    @property
    @override
    def expected_cardinality_repr(self) -> str:
        counts = ", ".join(map(str, self.counts[:-1])) + f" or {self.counts[-1]}"
        return f"either {counts} arguments"

    @property
    @override
    def is_variadic(self) -> bool:
        return False

    @override
    def must_stop_consumption(self, count: int, /) -> bool:
        return count >= max(self.counts)

    @override
    def is_valid(self, count: int, /) -> bool:
        return count in self.counts

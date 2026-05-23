from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from .base import BaseNumArgs


@dataclass(frozen=True)
class Optional(BaseNumArgs):
    @property
    def expected_cardinality_repr(self) -> str:
        return "0 or 1 argument"

    @property
    def is_variadic(self) -> bool:
        return False

    def must_stop_consumption(self, count: int, /) -> bool:
        return count >= 1

    def is_valid(self, count: int, /) -> bool:
        return 0 <= count <= 1


OPTIONAL: Final[Optional] = Optional()

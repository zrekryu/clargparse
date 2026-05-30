from __future__ import annotations

from dataclasses import dataclass
from typing import Final, override

from .base import BaseNumArgs


@dataclass(frozen=True)
class Optional(BaseNumArgs):
    @property
    @override
    def expected_cardinality_repr(self) -> str:
        return "0 or 1 argument"

    @property
    @override
    def is_variadic(self) -> bool:
        return False

    @override
    def must_stop_consumption(self, count: int, /) -> bool:
        return count >= 1

    @override
    def is_valid(self, count: int, /) -> bool:
        return 0 <= count <= 1


OPTIONAL: Final[Optional] = Optional()

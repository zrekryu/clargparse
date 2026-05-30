from __future__ import annotations

from dataclasses import dataclass
from typing import Final, override

from .base import BaseNumArgs


@dataclass(frozen=True)
class OneOrMore(BaseNumArgs):
    @property
    @override
    def expected_cardinality_repr(self) -> str:
        return "1 or more arguments"

    @property
    @override
    def is_variadic(self) -> bool:
        return True

    @override
    def must_stop_consumption(
        self,
        count: int,
        /,
    ) -> bool:
        return False

    @override
    def is_valid(self, count: int, /) -> bool:
        return count >= 1


ONE_OR_MORE: Final[OneOrMore] = OneOrMore()

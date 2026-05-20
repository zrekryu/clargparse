from dataclasses import dataclass
from typing import Final

from .base import BaseNumArgs


@dataclass(frozen=True)
class OneOrMore(BaseNumArgs):
    @property
    def expected_cardinality_repr(self) -> str:
        return "1 or more arguments"

    @property
    def is_variadic(self) -> bool:
        return True

    def must_stop_consumption(
        self,
        count: int,  # noqa: ARG002
        /,
    ) -> bool:
        return False

    def is_valid(self, count: int, /) -> bool:
        return count >= 1


ONE_OR_MORE: Final[OneOrMore] = OneOrMore()

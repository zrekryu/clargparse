from __future__ import annotations

from dataclasses import dataclass
from typing import override

from .base import BaseNumArgs


@dataclass(frozen=True)
class Range(BaseNumArgs):
    minimum: int
    maximum: int

    def __init__(self, minimum: int, maximum: int) -> None:
        if minimum < 1:
            exc_message = f"minimum must be at least 1, got {minimum}"
            raise ValueError(exc_message)
        if maximum < 1:
            exc_message = f"maximum must be at least 1, got {maximum}"
            raise ValueError(exc_message)

        if minimum > maximum:
            exc_message = f"minimum ({minimum}) cannot exceed maximum ({maximum})"
            raise ValueError(exc_message)
        if minimum == maximum:
            exc_message = "minimum and maximum cannot be equal"
            raise ValueError(exc_message)

        object.__setattr__(self, "minimum", minimum)
        object.__setattr__(self, "maximum", maximum)

    @property
    @override
    def expected_cardinality_repr(self) -> str:
        return f"{self.minimum}-{self.maximum} arguments"

    @property
    @override
    def is_variadic(self) -> bool:
        return False

    @override
    def must_stop_consumption(self, count: int, /) -> bool:
        return count >= self.maximum

    @override
    def is_valid(self, count: int, /) -> bool:
        return self.minimum <= count <= self.maximum

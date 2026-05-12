from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import ParameterError


if TYPE_CHECKING:
    from cliargparse.models.parameters import Positional


class PositionalAfterVariadicPositionalError(ParameterError):
    def __init__(self, positional: Positional[Any]) -> None:
        super().__init__(positional)

        self.positional = positional

    def __str__(self) -> str:
        return f"cannot add positional after variadic positional {self.positional.name!r}"


class DuplicatePositionalNameError(ParameterError):
    def __init__(
        self,
        name: str,
        existing: Positional[Any],
        duplicate: Positional[Any],
    ) -> None:
        super().__init__(name, existing, duplicate)

        self.name = name
        self.existing = existing
        self.duplicate = duplicate

    def __str__(self) -> str:
        return f"name {self.name!r} is already taken by positional {self.existing!r}"

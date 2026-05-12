from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .base import ParameterError


if TYPE_CHECKING:
    from cliargparse.models.parameters import Option


class DuplicateOptionSpecifierError(ParameterError):
    def __init__(
        self,
        specifier: str,
        existing: Option[Any],
        duplicate: Option[Any],
    ) -> None:
        super().__init__(specifier, existing, duplicate)

        self.specifier = specifier
        self.existing = existing
        self.duplicate = duplicate

    def __str__(self) -> str:
        return f"specifier {self.specifier!r} already exists"

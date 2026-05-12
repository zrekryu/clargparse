from __future__ import annotations

from typing import TYPE_CHECKING

from .base import ParameterError


if TYPE_CHECKING:
    from cliargparse.models.parameters import Command


class ParseModeError(ParameterError):
    def __init__(self, message: str) -> None:
        super().__init__(message)

        self.message = message

    def __str__(self) -> str:
        return self.message


class DuplicateSubcommandNameError(ParameterError):
    def __init__(
        self,
        name: str,
        existing: Command,
        duplicate: Command,
    ) -> None:
        super().__init__(name, existing, duplicate)

        self.name = name
        self.existing = existing
        self.duplicate = duplicate

    def __str__(self) -> str:
        return f"name {self.name!r} already exists"

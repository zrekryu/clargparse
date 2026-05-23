from __future__ import annotations

from dataclasses import dataclass

from cliargparse.enums import OptionPrefix

from .token import Token


@dataclass(frozen=True)
class OptionToken(Token):
    prefix: OptionPrefix
    name: str
    value: str | None = None

    @property
    def specifier(self) -> str:
        return f"{self.prefix}{self.name}"

    @property
    def is_long(self) -> bool:
        return self.prefix == OptionPrefix.LONG

    @property
    def is_short(self) -> bool:
        return self.prefix == OptionPrefix.SHORT

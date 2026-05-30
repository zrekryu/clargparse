from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .token import LexerToken


if TYPE_CHECKING:
    from .option import OptionToken


@dataclass(frozen=True)
class ShortOptionGroupToken(LexerToken):
    options: tuple[OptionToken, ...]

    @property
    def option_names(self) -> str:
        return "".join(option.name for option in self.options)

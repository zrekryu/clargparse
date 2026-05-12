from dataclasses import dataclass

from .option import OptionToken
from .token import Token


@dataclass(frozen=True)
class ShortOptionGroupToken(Token):
    options: tuple[OptionToken, ...]

    @property
    def option_names(self) -> str:
        return "".join(option.name for option in self.options)

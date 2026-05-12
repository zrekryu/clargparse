from dataclasses import dataclass

from .token import Token


@dataclass(frozen=True)
class ArgumentToken(Token):
    pass

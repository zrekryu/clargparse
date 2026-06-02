from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any


if TYPE_CHECKING:
    from clargparse.lexer.tokens import ArgumentToken
    from clargparse.models.parameters import Positional


@dataclass(frozen=True)
class PositionalNode:
    positional: Positional[Any]
    argument_tokens: tuple[ArgumentToken, ...]
    value: Any

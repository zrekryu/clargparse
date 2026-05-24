from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any


if TYPE_CHECKING:
    from cliargparse.lexer.tokens import ArgumentToken
    from cliargparse.models.parameters import Positional


@dataclass(frozen=True)
class PositionalNode:
    token: ArgumentToken
    positional: Positional[Any]
    values: Any

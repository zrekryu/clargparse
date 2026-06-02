from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any


if TYPE_CHECKING:
    from clargparse.lexer.tokens import ArgumentToken, OptionToken
    from clargparse.models.parameters import Option


@dataclass(frozen=True)
class OptionNode:
    token: OptionToken
    option: Option[Any]
    argument_tokens: tuple[ArgumentToken, ...]
    value: Any

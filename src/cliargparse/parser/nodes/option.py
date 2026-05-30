from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any


if TYPE_CHECKING:
    from cliargparse.lexer.tokens import ArgumentToken, OptionToken
    from cliargparse.models.parameters import Option


@dataclass(frozen=True)
class OptionNode:
    token: OptionToken
    option: Option[Any]
    argument_tokens: tuple[ArgumentToken, ...]
    values: Any

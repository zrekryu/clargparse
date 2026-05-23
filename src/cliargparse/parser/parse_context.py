from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .nodes import CommandNode
    from .token_stream import TokenStream


@dataclass
class ParseContext:
    token_stream: TokenStream
    node: CommandNode
    positional_index: int = 0

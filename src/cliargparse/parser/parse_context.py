from __future__ import annotations

from dataclasses import KW_ONLY, dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .nodes import CommandNode
    from .token_stream import TokenStream


@dataclass
class ParseContext:
    node: CommandNode
    token_stream: TokenStream

    _: KW_ONLY

    positional_index: int = 0

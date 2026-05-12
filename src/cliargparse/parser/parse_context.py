from dataclasses import dataclass

from .nodes import CommandNode
from .token_stream import TokenStream


@dataclass
class ParseContext:
    token_stream: TokenStream
    node: CommandNode
    positional_index: int = 0

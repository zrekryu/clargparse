from dataclasses import dataclass
from typing import Any

from cliargparse.models.parameters import Positional


@dataclass(frozen=True)
class PositionalNode:
    positional: Positional[Any]
    values: Any

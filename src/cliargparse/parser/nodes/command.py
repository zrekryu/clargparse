from __future__ import annotations

from dataclasses import KW_ONLY, dataclass, field
from typing import Any

from cliargparse.models.parameters import Command, Option, Positional

from .option import OptionNode
from .positional import PositionalNode


@dataclass
class CommandNode:
    command: Command

    _: KW_ONLY

    options: dict[Option[Any], OptionNode] = field(
        default_factory=dict[Option[Any], OptionNode],
    )

    subcommand: CommandNode | None = None

    positionals: dict[Positional[Any], PositionalNode] = field(
        default_factory=dict[Positional[Any], PositionalNode],
    )

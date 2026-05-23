from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any


if TYPE_CHECKING:
    from cliargparse.models.parameters import Option


@dataclass(frozen=True)
class OptionNode:
    specifier: str
    option: Option[Any]
    values: Any

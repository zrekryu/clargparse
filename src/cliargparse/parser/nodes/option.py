from dataclasses import dataclass
from typing import Any

from cliargparse.models.parameters import Option


@dataclass(frozen=True)
class OptionNode:
    specifier: str
    option: Option[Any]
    values: Any

from enum import StrEnum, auto
from typing import assert_never


class ParseMode(StrEnum):
    COMMAND = auto()
    POSITIONAL = auto()


class OptionPrefix(StrEnum):
    SHORT = "-"
    LONG = "--"


class NArgs(StrEnum):
    OPTIONAL = "?"

    ZERO_OR_MORE = "*"
    ONE_OR_MORE = "+"

    @property
    def is_variadic(self) -> bool:
        match self:
            case NArgs.OPTIONAL | NArgs.ZERO_OR_MORE | NArgs.ONE_OR_MORE:
                return True
            case _:
                assert_never(self)

    def is_valid_count(self, count: int) -> bool:
        match self:
            case NArgs.OPTIONAL:
                return 0 <= count <= 1
            case NArgs.ZERO_OR_MORE:
                return count >= 0
            case NArgs.ONE_OR_MORE:
                return count >= 1
            case _:
                assert_never(self)

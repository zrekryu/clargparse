from __future__ import annotations

from enum import StrEnum, auto


class TokenizerState(StrEnum):
    UNQUOTED = auto()
    SINGLE_QUOTE = auto()
    DOUBLE_QUOTE = auto()


class ParseMode(StrEnum):
    COMMAND = auto()
    POSITIONAL = auto()


class OptionPrefix(StrEnum):
    LONG = "--"
    SHORT = "-"

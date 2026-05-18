from enum import StrEnum, auto


class ParseMode(StrEnum):
    COMMAND = auto()
    POSITIONAL = auto()


class OptionPrefix(StrEnum):
    SHORT = "-"
    LONG = "--"

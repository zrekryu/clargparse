from __future__ import annotations

from .lexer import LexerError, MissingOptionNameError, ShortOptionNameTooLongError
from .parameters import ParameterError, ParseModeError
from .parser import (
    InvalidOptionChoiceError,
    InvalidPositionalChoiceError,
    MissingOptionArgumentsError,
    MissingPositionalArgumentsError,
    MissingRequiredMutexOptionFromGroupError,
    MissingRequiredOptionsError,
    MissingRequiredPositionalsError,
    MutexOptionCannotCoexistError,
    OptionTakesNoArgumentsError,
    OptionTakingArgumentInGroupError,
    ParserError,
    SubcommandRequiredError,
    UnexpectedPositionalArgumentError,
    UnknownCommandError,
    UnknownLongOptionError,
    UnknownOptionError,
    UnknownShortOptionError,
    UnknownShortOptionInGroupError,
)
from .tokenizer import (
    InvalidEscapeSequenceError,
    TokenizerError,
    UnclosedQuoteError,
    UnterminatedEscapeSequenceError,
)


__all__ = [
    "InvalidEscapeSequenceError",
    "InvalidOptionChoiceError",
    "InvalidPositionalChoiceError",
    "LexerError",
    "MissingOptionArgumentsError",
    "MissingOptionNameError",
    "MissingPositionalArgumentsError",
    "MissingRequiredMutexOptionFromGroupError",
    "MissingRequiredOptionsError",
    "MissingRequiredPositionalsError",
    "MutexOptionCannotCoexistError",
    "OptionTakesNoArgumentsError",
    "OptionTakingArgumentInGroupError",
    "ParameterError",
    "ParseModeError",
    "ParserError",
    "ShortOptionNameTooLongError",
    "SubcommandRequiredError",
    "TokenizerError",
    "UnclosedQuoteError",
    "UnexpectedPositionalArgumentError",
    "UnknownCommandError",
    "UnknownLongOptionError",
    "UnknownOptionError",
    "UnknownShortOptionError",
    "UnknownShortOptionInGroupError",
    "UnterminatedEscapeSequenceError",
]

from __future__ import annotations

from dataclasses import dataclass

from cliargparse.enums import OptionPrefix
from cliargparse.lexer.delimiters import OPTION_ARGUMENT
from cliargparse.tokenizer.tokens import TokenizerToken

from .argument import ArgumentToken
from .token import LexerToken


@dataclass(frozen=True)
class OptionToken(LexerToken):
    prefix: OptionPrefix
    name: str
    argument: str | None = None

    @property
    def specifier(self) -> str:
        return f"{self.prefix}{self.name}"

    @property
    def is_long(self) -> bool:
        return self.prefix == OptionPrefix.LONG

    @property
    def is_short(self) -> bool:
        return self.prefix == OptionPrefix.SHORT

    @property
    def argument_token(self) -> ArgumentToken | None:
        if self.argument is None:
            return None

        start_index = (self.token.start_index or 0) + self.token.value.find(OPTION_ARGUMENT) + 1
        return ArgumentToken(
            token=TokenizerToken(
                self.argument, start_index=start_index, end_index=start_index + len(self.argument)
            )
        )

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol


if TYPE_CHECKING:
    from collections.abc import Sequence

    from .lexer.tokens import ArgumentToken, OptionToken, ShortOptionGroupToken
    from .models.parameters import Parameter


type LexerTokenUnion = OptionToken | ShortOptionGroupToken | ArgumentToken


class Action[P: Parameter](Protocol):
    def __call__(
        self,
        parameter: P,
        tokens: Sequence[ArgumentToken],
        values: Sequence[Any],
        *,
        current_value: Any = None,
    ) -> Any: ...

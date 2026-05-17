from __future__ import annotations

from dataclasses import KW_ONLY, dataclass
from typing import TYPE_CHECKING

from cliargparse.actions import store_value_action
from cliargparse.enums import NArgs

from .parameter import Parameter


if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from cliargparse.hints import Action


@dataclass(frozen=True)
class Positional[T](Parameter):
    name: str

    _: KW_ONLY

    action: Action[Positional[T]]
    nargs: int | NArgs

    default: T | None = None

    type_converter: type[str] | Callable[[str], T]
    choices: tuple[T, ...]

    @property
    def is_required(self) -> bool:
        return isinstance(self.nargs, int) or self.nargs is NArgs.ONE_OR_MORE

    @classmethod
    def create(
        cls,
        name: str,
        *,
        action: Action[Positional[T]] | None = None,
        nargs: int | NArgs | None = None,
        default: T | None = None,
        type_converter: Callable[[str], T] | None = None,
        choices: Sequence[T] | None = None,
    ) -> Positional[T]:
        if action is None:
            action = store_value_action

        if nargs is None:
            nargs = 1

        if isinstance(nargs, int) and nargs <= 0:
            exc_message = f"expected positional nargs > 0, got {nargs}"
            raise ValueError(exc_message)

        return cls(
            name=name,
            action=action,
            nargs=nargs,
            default=default,
            type_converter=type_converter or str,
            choices=tuple(choices or ()),
        )

    def __str__(self) -> str:
        return self.name

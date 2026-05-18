from __future__ import annotations

from dataclasses import KW_ONLY, dataclass
from typing import TYPE_CHECKING

from cliargparse.actions import store_value_action

from .parameter import Parameter


if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from cliargparse import numargs
    from cliargparse.hints import Action


@dataclass(frozen=True)
class Positional[T](Parameter):
    name: str

    _: KW_ONLY

    action: Action[Positional[T]]
    num_args: int | numargs.BaseNumArgs

    default: T | None = None

    type_converter: type[str] | Callable[[str], T]
    choices: tuple[T, ...]

    @property
    def is_required(self) -> bool:
        return self.default is None

    @classmethod
    def create(
        cls,
        name: str,
        *,
        action: Action[Positional[T]] | None = None,
        num_args: int | numargs.BaseNumArgs | None = None,
        default: T | None = None,
        type_converter: Callable[[str], T] | None = None,
        choices: Sequence[T] | None = None,
    ) -> Positional[T]:
        if action is None:
            action = store_value_action

        if num_args is None:
            num_args = 1

        if isinstance(num_args, int) and num_args <= 0:
            exc_message = f"expected positional num_args > 0, got {num_args}"
            raise ValueError(exc_message)

        return cls(
            name=name,
            action=action,
            num_args=num_args,
            default=default,
            type_converter=type_converter or str,
            choices=tuple(choices or ()),
        )

    def __str__(self) -> str:
        return self.name

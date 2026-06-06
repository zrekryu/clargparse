from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from .parameters import Command, Option


if TYPE_CHECKING:
    from collections.abc import Callable, Iterator, Sequence

    from clargparse.typing import Action


@dataclass(frozen=True)
class MutexOptionGroup:
    command: Command
    required: bool = False

    _options: list[Option[Any]] = field(default_factory=list[Option[Any]], init=False, repr=False)

    @property
    def options(self) -> tuple[Option[Any], ...]:
        return tuple(self._options)

    def add_option(self, option: Option[Any]) -> None:
        self.command.add_option(option)
        self._options.append(option)

    def option[T](
        self,
        long_names: str | Sequence[str] | None = None,
        short_names: str | Sequence[str] | None = None,
        *,
        long_aliases: str | Sequence[str] | None = None,
        short_aliases: str | Sequence[str] | None = None,
        store_name: str | None = None,
        action: Action[Option[T]] | None = None,
        present: Any | None = None,
        default: Any | None = None,
        type_converter: Callable[[str], T] | None = None,
        choices: Sequence[T] | None = None,
    ) -> Option[T]:
        option = Option[T].create(
            long_names=long_names,
            short_names=short_names,
            long_aliases=long_aliases,
            short_aliases=short_aliases,
            store_name=store_name,
            action=action,
            num_args=0,
            present=present,
            default=default,
            type_converter=type_converter,
            choices=choices,
        )
        self.add_option(option)

        return option

    def __iter__(self) -> Iterator[Option[Any]]:
        return iter(self._options)

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal


if TYPE_CHECKING:
    from collections.abc import Sequence

    from .lexer.tokens import ArgumentToken
    from .models.parameters import Option, Positional


def store_value_action(
    parameter: Option[Any] | Positional[Any],  # noqa: ARG001
    tokens: Sequence[ArgumentToken],  # noqa: ARG001
    arguments: Sequence[Any],
    *,
    current_value: Any = None,  # noqa: ARG001
) -> Any | None:
    return arguments[0] if arguments else None


def store_true_action(
    parameter: Option[Any],  # noqa: ARG001
    tokens: Sequence[ArgumentToken],  # noqa: ARG001
    arguments: Sequence[Any],  # noqa: ARG001
    *,
    current_value: bool | None = None,  # noqa: ARG001
) -> Literal[True]:
    return True


def store_false_action(
    parameter: Option[Any],  # noqa: ARG001
    tokens: Sequence[ArgumentToken],  # noqa: ARG001
    arguments: Sequence[Any],  # noqa: ARG001
    *,
    current_value: bool | None = None,  # noqa: ARG001
) -> Literal[False]:
    return False


def store_present_action(
    parameter: Option[Any],
    tokens: Sequence[ArgumentToken],  # noqa: ARG001
    arguments: Sequence[Any],  # noqa: ARG001
    *,
    current_value: Any = None,  # noqa: ARG001
) -> Any:
    return parameter.present


def append_value_action(
    parameter: Option[Any] | Positional[Any],  # noqa: ARG001
    tokens: Sequence[ArgumentToken],  # noqa: ARG001
    arguments: Sequence[Any],
    *,
    current_value: list[Any] | None = None,
) -> list[Any]:
    if current_value is None:
        current_value = []

    if arguments:
        current_value.append(arguments)

    return current_value


def append_present_action(
    parameter: Option[Any],
    tokens: Sequence[ArgumentToken],  # noqa: ARG001
    arguments: Sequence[Any],  # noqa: ARG001
    *,
    current_value: list[Any] | None = None,
) -> list[Any]:
    if current_value is None:
        current_value = []

    current_value.append(parameter.present)
    return current_value


def extend_values_action(
    parameter: Option[Any] | Positional[Any],  # noqa: ARG001
    tokens: Sequence[ArgumentToken],  # noqa: ARG001
    arguments: Sequence[Any],
    *,
    current_value: list[Any] | None = None,
) -> list[Any]:
    if current_value is None:
        current_value = []

    current_value.extend(arguments)
    return current_value


def count_presence_action(
    parameter: Option[Any],  # noqa: ARG001
    tokens: Sequence[ArgumentToken],  # noqa: ARG001
    arguments: Sequence[Any],  # noqa: ARG001
    *,
    current_value: int | None = None,
) -> int:
    return current_value + 1 if current_value else 1

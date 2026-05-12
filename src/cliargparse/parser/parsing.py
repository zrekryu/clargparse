from collections.abc import Callable, Iterable
from typing import Any, assert_never

from cliargparse.enums import NArgs, OptionPrefix, ParseMode
from cliargparse.exceptions import (
    InvalidOptionChoiceError,
    InvalidPositionalChoiceError,
    MissingOptionArgumentsError,
    MissingPositionalArgumentsError,
    MissingRequiredMutexOptionError,
    MissingRequiredOptionsError,
    MissingRequiredPositionalsError,
    MutexOptionCannotCoexistError,
    OptionTakesNoArgumentsError,
    OptionTakingArgumentInGroupError,
    SubcommandRequiredError,
    UnexpectedPositionalArgumentError,
    UnknownCommandError,
    UnknownLongOptionError,
    UnknownShortOptionError,
    UnknownShortOptionInGroupError,
)
from cliargparse.hints import LexerToken
from cliargparse.lexer.tokens import (
    ArgumentToken,
    OptionToken,
    ShortOptionGroupToken,
)
from cliargparse.models import MutexOptionGroup
from cliargparse.models.parameters import Command, Option, Positional

from .nodes import CommandNode, OptionNode, PositionalNode
from .parse_context import ParseContext
from .token_stream import TokenStream


def parse(tokens: Iterable[LexerToken], command: Command) -> CommandNode:
    node = CommandNode(command)
    token_stream = TokenStream(tokens)

    context = ParseContext(
        node=node,
        token_stream=token_stream,
    )

    while (token := token_stream.peek()) is not None:
        match token:
            case OptionToken(prefix=prefix):
                token_stream.consume()
                match prefix:
                    case OptionPrefix.LONG:
                        _handle_long_option(token, context)
                    case OptionPrefix.SHORT:
                        _handle_short_option(token, context)
                    case _:
                        assert_never(prefix)
            case ShortOptionGroupToken():
                token_stream.consume()
                _handle_short_option_group(token, context)
            case ArgumentToken():
                parse_mode = context.node.command.parse_mode
                match parse_mode:
                    case ParseMode.COMMAND:
                        token_stream.consume()
                        _handle_command(token, context)
                    case ParseMode.POSITIONAL:
                        _handle_positional(token, context)
                    case _:
                        assert_never(parse_mode)
            case _:
                assert_never(token)

    _validate_command_node(node)

    return node


def _handle_long_option(token: OptionToken, context: ParseContext) -> None:
    node = _parse_long_option(token, context)
    context.node.options[node.option] = node


def _parse_long_option(token: OptionToken, context: ParseContext) -> OptionNode:
    option = context.node.command.get_long_option(token.name)
    if not option:
        raise UnknownLongOptionError(token.name)

    arguments = _consume_and_validate_option_arguments(token, option, context.token_stream)

    current_value: Any | None = None
    if current_option := context.node.options.get(option):
        current_value = current_option.values

    values = option.action(option, arguments, current_value=current_value)

    return OptionNode(token.specifier, option, values)


def _handle_short_option(token: OptionToken, context: ParseContext) -> None:
    node = _parse_short_option(token, context)
    context.node.options[node.option] = node


def _parse_short_option(token: OptionToken, context: ParseContext) -> OptionNode:
    option = context.node.command.get_short_option(token.name)
    if not option:
        raise UnknownShortOptionError(token.name)

    arguments = _consume_and_validate_option_arguments(token, option, context.token_stream)

    current_value: Any | None = None
    if current_option := context.node.options.get(option):
        current_value = current_option.values

    values = option.action(option, arguments, current_value=current_value)

    return OptionNode(token.specifier, option, values)


def _handle_short_option_group(token: ShortOptionGroupToken, context: ParseContext) -> None:
    for node in _parse_short_option_group(token, context):
        context.node.options[node.option] = node


def _parse_short_option_group(
    token: ShortOptionGroupToken,
    context: ParseContext,
) -> tuple[OptionNode, ...]:
    nodes: list[OptionNode] = []
    for option_token in token.options:
        option = context.node.command.get_short_option(option_token.name)
        if not option:
            raise UnknownShortOptionInGroupError(option_token.name, token.option_names)

        if option.takes_arguments:
            raise OptionTakingArgumentInGroupError(option_token.name, token.option_names)

        current_value: Any | None = None
        if current_option := context.node.options.get(option):
            current_value = current_option.values

        values = option.action(option, (), current_value=current_value)

        node = OptionNode(option_token.specifier, option, values)
        nodes.append(node)

    return tuple(nodes)


def _consume_and_validate_option_arguments(
    token: OptionToken,
    option: Option[Any],
    token_stream: TokenStream,
) -> tuple[Any, ...]:
    if not option.takes_arguments and token.argument is not None:
        raise OptionTakesNoArgumentsError(token.specifier, token.argument)

    values: tuple[Any, ...]
    if option.takes_arguments:
        if token.argument is not None:
            values = (token.argument,)
        else:
            values = _consume_arguments(
                option.nargs,
                token_stream,
                type_converter=option.type_converter,
            )
    else:
        values = ()

    if not _is_valid_nargs_count(option.nargs, len(values)):
        raise MissingOptionArgumentsError(token.specifier, option.nargs, len(values))

    if option.choices:
        for value in values:
            if value not in option.choices:
                raise InvalidOptionChoiceError(
                    token.specifier,
                    value,
                    tuple(map(repr, option.choices)),
                )

    return tuple(values)


def _handle_command(token: ArgumentToken, context: ParseContext) -> None:
    command = _parse_command(token, context)

    context.node.subcommand = CommandNode(command)
    context.node = context.node.subcommand


def _parse_command(token: ArgumentToken, context: ParseContext) -> Command:
    command = context.node.command.get_subcommand(token.lexeme)
    if not command:
        raise UnknownCommandError(token.lexeme)

    return command


def _handle_positional(token: ArgumentToken, context: ParseContext) -> None:
    node = _parse_positional(token, context)
    context.node.positionals[node.positional] = node


def _parse_positional(token: ArgumentToken, context: ParseContext) -> PositionalNode:
    try:
        positional = context.node.command.get_positional_by_index(context.positional_index)
    except IndexError:
        raise UnexpectedPositionalArgumentError(token.lexeme) from None

    arguments = _consume_arguments(
        positional.nargs,
        context.token_stream,
        type_converter=positional.type_converter,
    )

    current_value: Any | None = None
    if current_positional := context.node.positionals.get(positional):
        current_value = current_positional.values

    values = positional.action(positional, arguments, current_value=current_value)

    if not _is_valid_nargs_count(positional.nargs, len(values)):
        raise MissingPositionalArgumentsError(positional.name, positional.nargs, len(values))

    if positional.choices:
        for value in values:
            if value not in positional.choices:
                raise InvalidPositionalChoiceError(
                    positional.name,
                    value,
                    tuple(map(repr, positional.choices)),
                )

    context.positional_index += 1

    return PositionalNode(positional, values)


def _consume_arguments(
    nargs: int | NArgs,
    token_stream: TokenStream,
    *,
    type_converter: Callable[[str], Any] = str,
) -> tuple[Any, ...]:
    values: list[Any] = []
    while (token := token_stream.peek()) is not None:
        if not isinstance(token, ArgumentToken):
            break

        match nargs:
            case NArgs.OPTIONAL:
                if values:
                    break
            case NArgs.ZERO_OR_MORE | NArgs.ONE_OR_MORE:
                pass
            case int():
                if len(values) >= nargs:
                    break
            case _:
                assert_never(nargs)

        values.append(type_converter(token.lexeme))

        token_stream.consume()

    return tuple(values)


def _is_valid_nargs_count(nargs: int | NArgs, count: int) -> bool:
    if isinstance(nargs, NArgs):
        return nargs.is_valid_count(count)

    return count >= nargs


def _validate_command_node(node: CommandNode) -> None:
    if options := node.command.options:
        _validate_options(options, node.options)

    if mutex_option_groups := node.command.mutex_option_groups:
        _validate_mutex_option_groups(mutex_option_groups, node.options)

    if node.command.subcommand_required and not node.subcommand:
        raise SubcommandRequiredError(
            name=node.command.name,
            subcommands=node.command.subcommands,
        )

    if subcommand := node.subcommand:
        _validate_command_node(subcommand)

    if positionals := node.command.positionals:
        _validate_positionals(positionals, node.positionals)


def _validate_options(
    options: Iterable[Option[Any]],
    option_nodes: dict[Option[Any], OptionNode],
) -> None:
    missing = tuple(option for option in options if option.required and option not in option_nodes)
    if missing:
        raise MissingRequiredOptionsError(missing)


def _validate_mutex_option_groups(
    mutex_option_groups: Iterable[MutexOptionGroup],
    option_nodes: dict[Option[Any], OptionNode],
) -> None:
    for group in mutex_option_groups:
        found_specifiers = tuple(
            node.specifier for parameter, node in option_nodes.items() if parameter in group.options
        )
        if len(found_specifiers) > 1:
            raise MutexOptionCannotCoexistError(found_specifiers[0], found_specifiers[1:])

        if group.required and not found_specifiers:
            raise MissingRequiredMutexOptionError(group)


def _validate_positionals(
    positionals: Iterable[Positional[Any]],
    positional_nodes: dict[Positional[Any], PositionalNode],
) -> None:
    missing = tuple(
        positional
        for positional in positionals
        if positional.is_required and positional not in positional_nodes
    )
    if missing:
        raise MissingRequiredPositionalsError(missing)

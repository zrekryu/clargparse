from __future__ import annotations

from clargparse.enums import OptionPrefix
from clargparse.lexer import lex
from clargparse.lexer.tokens import ArgumentToken, OptionToken, ShortOptionGroupToken
from clargparse.tokenizer import tokenize


def test_lex_long_option_name_starts_with_digit() -> None:
    tokenizer_tokens = tokenize("--1")
    tokens = list(lex(tokenizer_tokens))
    assert tokens == [ArgumentToken(token=tokenizer_tokens[0])]


def test_lex_long_option() -> None:
    tokenizer_tokens = tokenize("--long")
    tokens = list(lex(tokenizer_tokens))
    assert tokens == [
        OptionToken(token=tokenizer_tokens[0], prefix=OptionPrefix.LONG, name="long", argument=None)
    ]


def test_lex_long_option_with_argument() -> None:
    tokenizer_tokens = tokenize("--long=arg")
    tokens = list(lex(tokenizer_tokens))
    assert tokens == [
        OptionToken(
            token=tokenizer_tokens[0], prefix=OptionPrefix.LONG, name="long", argument="arg"
        )
    ]


def test_lex_short_option_name_starts_with_digit() -> None:
    tokenizer_tokens = tokenize("-1")
    tokens = list(lex(tokenizer_tokens))
    assert tokens == [ArgumentToken(token=tokenizer_tokens[0])]


def test_lex_short_option() -> None:
    tokenizer_tokens = tokenize("-s")
    tokens = list(lex(tokenizer_tokens))
    assert tokens == [
        OptionToken(token=tokenizer_tokens[0], prefix=OptionPrefix.SHORT, name="s", argument=None)
    ]


def test_lex_short_option_with_argument() -> None:
    tokenizer_tokens = tokenize("-s=arg")
    tokens = list(lex(tokenizer_tokens))
    assert tokens == [
        OptionToken(token=tokenizer_tokens[0], prefix=OptionPrefix.SHORT, name="s", argument="arg")
    ]


def test_lex_short_option_group() -> None:
    tokenizer_tokens = tokenize("-ab")
    tokens = list(lex(tokenizer_tokens))
    assert tokens == [
        ShortOptionGroupToken(
            token=tokenizer_tokens[0],
            options=(
                OptionToken(
                    token=tokenizer_tokens[0], prefix=OptionPrefix.SHORT, name="a", argument=None
                ),
                OptionToken(
                    token=tokenizer_tokens[0], prefix=OptionPrefix.SHORT, name="b", argument=None
                ),
            ),
        )
    ]


def test_lex_end_of_options() -> None:
    tokenizer_tokens = tokenize("-- -- --long -s")
    tokens = list(lex(tokenizer_tokens))
    assert tokens == [
        ArgumentToken(token=tokenizer_tokens[1]),
        ArgumentToken(token=tokenizer_tokens[2]),
        ArgumentToken(token=tokenizer_tokens[3]),
    ]

import pytest

from cliargparse.exceptions import (
    InvalidEscapeSequenceError,
    UnclosedQuoteError,
    UnterminatedEscapeSequenceError,
)
from cliargparse.tokenizer import tokenize
from cliargparse.tokenizer.tokens import TokenizerToken


def test_tokenize_unquoted() -> None:
    tokens = tokenize("hello world")
    assert tokens == [
        TokenizerToken(value="hello", start_index=0, end_index=5),
        TokenizerToken(value="world", start_index=6, end_index=11),
    ]


def test_tokenize_unquoted_escaped_single_quote() -> None:
    tokens = tokenize(r"hello\'world")
    assert tokens == [TokenizerToken(value="hello'world", start_index=0, end_index=12)]


def test_tokenize_unquoted_escaped_double_quote() -> None:
    tokens = tokenize(r"hello\"world")
    assert tokens == [TokenizerToken(value='hello"world', start_index=0, end_index=12)]


def test_tokenize_unquoted_escaped_backslash() -> None:
    tokens = tokenize(r"hello\\world")
    assert tokens == [TokenizerToken(value="hello\\world", start_index=0, end_index=12)]


def test_tokenize_unquoted_escaped_space() -> None:
    tokens = tokenize(r"hello\ world")
    assert tokens == [TokenizerToken(value="hello world", start_index=0, end_index=12)]


def test_tokenize_unquoted_unterminated_escape() -> None:
    with pytest.raises(UnterminatedEscapeSequenceError):
        tokenize("hello\\")


def test_tokenize_unquoted_invalid_escape() -> None:
    with pytest.raises(InvalidEscapeSequenceError):
        tokenize(r"hello\i")


def test_tokenize_single_quote() -> None:
    tokens = tokenize("'hello world'")
    assert tokens == [TokenizerToken(value="hello world", start_index=1, end_index=12)]


def test_tokenize_single_quote_unclosed() -> None:
    with pytest.raises(UnclosedQuoteError):
        tokenize("'hello")


def test_tokenize_double_quote() -> None:
    tokens = tokenize('"hello world"')
    assert tokens == [TokenizerToken(value="hello world", start_index=1, end_index=12)]


def test_tokenize_double_quote_escaped_single_quote() -> None:
    tokens = tokenize(r'"hello\'world"')
    assert tokens == [TokenizerToken(value="hello'world", start_index=1, end_index=13)]


def test_tokenize_double_quote_escaped_double_quote() -> None:
    tokens = tokenize(r'"hello\"world"')
    assert tokens == [TokenizerToken(value='hello"world', start_index=1, end_index=13)]


def test_tokenize_double_quote_escaped_backslash() -> None:
    tokens = tokenize(r'"hello\\world"')
    assert tokens == [TokenizerToken(value=r"hello\world", start_index=1, end_index=13)]


def test_tokenize_double_quote_escaped_space() -> None:
    tokens = tokenize(r'"hello\ world"')
    assert tokens == [TokenizerToken(value="hello world", start_index=1, end_index=13)]


def test_tokenize_double_quote_unterminated_escape() -> None:
    with pytest.raises(UnterminatedEscapeSequenceError):
        tokenize('"hello\\')


def test_tokenize_double_quote_invalid_escape() -> None:
    with pytest.raises(InvalidEscapeSequenceError):
        tokenize(r'"hello\i"')


def test_tokenize_double_quote_unclosed() -> None:
    with pytest.raises(UnclosedQuoteError):
        tokenize('"hello')

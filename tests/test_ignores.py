"""Tests for _dummytest.ignores."""

import pathlib
import tempfile

from _dummytest.ignores import load_ignore_rules, is_ignored


def test_load_ignore_rules_from_file():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("ImportError[tests/test_x.py]\nAssertionError\n# comment\n\n")
        f.flush()
        path = pathlib.Path(f.name)

    rules = load_ignore_rules(str(path))
    assert len(rules) == 2
    assert rules[0] == ("ImportError", "tests/test_x.py")
    assert rules[1] == ("AssertionError", None)

    path.unlink()


def test_load_ignore_rules_nonexistent():
    rules = load_ignore_rules("no_such_file_abc.txt")
    assert rules == []


def test_is_ignored_by_exception_name():
    rules = [("ValueError", None)]
    assert is_ignored(rules, "ValueError", "test.py") is True
    assert is_ignored(rules, "TypeError", "test.py") is False


def test_is_ignored_wildcard():
    rules = [("*", None)]
    assert is_ignored(rules, "ValueError", "test.py") is True
    assert is_ignored(rules, "AssertionError", "test.py") is True


def test_is_ignored_with_glob():
    rules = [("ImportError", "tests/legacy/*.py")]
    assert is_ignored(rules, "ImportError", "") is False


def test_is_ignored_empty_rules():
    assert is_ignored([], "ValueError", "test.py") is False

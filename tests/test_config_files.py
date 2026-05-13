"""Tests for dummytest.ini and .dummytestignore loading."""

import pathlib

from _dummytest.config import config as cfg
from _dummytest.ignores import load_ignore_rules


_ROOT = pathlib.Path(__file__).parent.parent


def test_dummytest_ini_exists():
    assert (_ROOT / "dummytest.ini").is_file()


def test_dummytest_ini_loads():
    cfg._config = cfg.cp.ConfigParser()
    cfg._config.read(_ROOT / "dummytest.ini")
    assert cfg._config.has_section("dummytest")


def test_dummytest_ini_test_dir():
    cfg._config = cfg.cp.ConfigParser()
    cfg._config.read(_ROOT / "dummytest.ini")
    assert cfg._read_str_config("test_dir") == "tests"


def test_dummytest_ini_test_pattern():
    cfg._config = cfg.cp.ConfigParser()
    cfg._config.read(_ROOT / "dummytest.ini")
    assert cfg._read_str_config("test_pattern") == "test_*.py"


def test_dummytestignore_exists():
    assert (_ROOT / ".dummytestignore").is_file()


def test_dummytestignore_loads():
    rules = load_ignore_rules(str(_ROOT / ".dummytestignore"))
    assert isinstance(rules, list)


def test_dummytestignore_comments_skipped():
    rules = load_ignore_rules(str(_ROOT / ".dummytestignore"))
    assert rules == []

"""Tests for _dummytest.plugins."""

import builtins

from _dummytest.plugins import (
    reveal_type,
    dump_locals,
    record_calls,
    _install_plugins,
    _uninstall_plugins,
    _PLUGIN_NAMES,
)
from _dummytest.const import PLUGINABLE


# --- install / uninstall ---

def test_install_plugins_sets_builtins():
    _install_plugins()
    for name in _PLUGIN_NAMES:
        assert hasattr(builtins, name)
    _uninstall_plugins()


def test_uninstall_plugins_removes_builtins():
    _install_plugins()
    _uninstall_plugins()
    for name in _PLUGIN_NAMES:
        assert not hasattr(builtins, name)


def test_install_sets_pluginable_true():
    _install_plugins()
    assert bool(PLUGINABLE) is True
    _uninstall_plugins()


def test_uninstall_sets_pluginable_false():
    _install_plugins()
    _uninstall_plugins()
    assert bool(PLUGINABLE) is False


# --- reveal_type ---

def test_reveal_type_returns_value():
    result = reveal_type(42)
    assert result == 42


def test_reveal_type_prints_type(capsys):
    reveal_type("hello")
    out, _ = capsys.readouterr()
    assert "str" in out
    assert "hello" in out


def test_reveal_type_prints_format(capsys):
    reveal_type(3.14)
    out, _ = capsys.readouterr()
    assert "reveal_type |" in out
    assert "float" in out


# --- dump_locals ---

def test_dump_locals_prints_locals(capsys):
    x = 10
    y = "hello"
    dump_locals()
    out, _ = capsys.readouterr()
    assert "dump_locals |" in out
    assert "x = 10" in out
    assert "y = 'hello'" in out


def test_dump_locals_skips_dunder(capsys):
    __secret = "hidden"
    visible = "shown"
    dump_locals()
    out, _ = capsys.readouterr()
    assert "__secret" not in out
    assert "visible" in out


# --- record_calls ---

def test_record_calls_returns_result():
    @record_calls
    def add(a, b):
        return a + b
    assert add(1, 2) == 3


def test_record_calls_prints_call(capsys):
    @record_calls
    def add(a, b):
        return a + b
    add(1, 2)
    out, _ = capsys.readouterr()
    assert "record_calls |" in out
    assert "add(1, 2)" in out
    assert "-> 3" in out


def test_record_calls_prints_kwargs(capsys):
    @record_calls
    def greet(name="world"):
        return f"hi {name}"
    greet(name="alice")
    out, _ = capsys.readouterr()
    assert "name='alice'" in out


def test_record_calls_prints_exception(capsys):
    @record_calls
    def boom():
        raise ValueError("oops")
    try:
        boom()
    except ValueError:
        pass
    out, _ = capsys.readouterr()
    assert "raised ValueError" in out


def test_record_calls_preserves_name():
    @record_calls
    def my_func():
        pass
    assert my_func.__name__ == "my_func"


# --- __doc__ tests ---

def test_reveal_type_has_doc():
    assert reveal_type.__doc__ is not None


def test_dump_locals_has_doc():
    assert dump_locals.__doc__ is not None


def test_record_calls_has_doc():
    assert record_calls.__doc__ is not None

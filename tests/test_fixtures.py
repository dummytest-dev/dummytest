"""Tests for the dummytest fixture system."""

import os
import pathlib

import dummytest


# --- Test conftest fixtures (defined in conftest.py) ---

def test_conftest_fixture_sample_list(sample_list):
    assert sample_list == [1, 2, 3]


def test_conftest_fixture_sample_dict(sample_dict):
    assert sample_dict["a"] == 1
    assert sample_dict["b"] == 2


# --- Test built-in tmp_path fixture ---

def test_tmp_path_exists(tmp_path):
    assert isinstance(tmp_path, pathlib.Path)
    assert tmp_path.is_dir()


def test_tmp_path_writable(tmp_path):
    f = tmp_path / "hello.txt"
    f.write_text("hello")
    assert f.read_text() == "hello"


# --- Test built-in capsys fixture ---

def test_capsys_capture(capsys):
    print("hello stdout")
    import sys
    print("hello stderr", file=sys.stderr)
    out, err = capsys.readouterr()
    assert "hello stdout" in out
    assert "hello stderr" in err


def test_capsys_resets(capsys):
    print("first")
    capsys.readouterr()
    print("second")
    out, _ = capsys.readouterr()
    assert "second" in out
    assert "first" not in out


# --- Test built-in monkeypatch fixture ---

class _DummyObj:
    x = 10


def test_monkeypatch_setattr(monkeypatch):
    monkeypatch.setattr(_DummyObj, "x", 99)
    assert _DummyObj.x == 99


def test_monkeypatch_restores_after():
    assert _DummyObj.x == 10


def test_monkeypatch_setenv(monkeypatch):
    monkeypatch.setenv("DUMMYTEST_VAR", "hello")
    assert os.environ["DUMMYTEST_VAR"] == "hello"


def test_monkeypatch_env_restores_after():
    assert "DUMMYTEST_VAR" not in os.environ


# --- Test yield-based fixture teardown ---

_teardown_log = []


@dummytest.fixture
def tracked_resource():
    _teardown_log.append("setup")
    yield "resource"
    _teardown_log.append("teardown")


def test_yield_fixture_setup(tracked_resource):
    assert tracked_resource == "resource"
    assert "setup" in _teardown_log


def test_yield_fixture_teardown_ran():
    assert "teardown" in _teardown_log


# --- Test fixture depending on another fixture ---

@dummytest.fixture
def base_value():
    return 42


@dummytest.fixture
def doubled(base_value):
    return base_value * 2


def test_fixture_dependency(doubled):
    assert doubled == 84


# --- Test that tests with no params still work ---

def test_no_fixtures_needed():
    assert 1 + 1 == 2

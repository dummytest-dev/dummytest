"""Tests for _dummytest.run."""

import warnings

from _dummytest.run import _run_single_test


def _passing_test():
    assert 1 + 1 == 2


def _failing_test():
    assert 1 + 1 == 3


def _warning_test():
    warnings.warn("test warning", UserWarning)


def _exception_test():
    raise ValueError("oops")


def test_run_single_test_pass():
    result = _run_single_test(_passing_test)
    assert result["ok"] is True
    assert result["func_name"] == "_passing_test"
    assert result["tb"] is None
    assert result["warnings"] == []


def test_run_single_test_fail():
    result = _run_single_test(_failing_test)
    assert result["ok"] is False
    assert "AssertionError" in result["exc_name"]
    assert result["tb"] is not None
    assert result["explain"] is not None


def test_run_single_test_exception():
    result = _run_single_test(_exception_test)
    assert result["ok"] is False
    assert result["exc_name"] == "ValueError"
    assert "oops" in result["tb"]


def test_run_single_test_captures_warnings():
    result = _run_single_test(_warning_test)
    assert result["ok"] is True
    assert len(result["warnings"]) == 1
    assert result["warnings"][0].category is UserWarning


class TestInClass:
    def test_method(self):
        assert True


def test_run_class_method():
    result = _run_single_test(TestInClass.test_method)
    assert result["ok"] is True

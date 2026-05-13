"""Tests for _dummytest.explain."""

from _dummytest.explain import _explain_assertion


def test_explain_simple_comparison():
    try:
        assert 1 + 1 == 3
    except AssertionError:
        import sys
        result = _explain_assertion(sys.exc_info()[2])
        assert result is not None
        assert "2 == 3" in result


def test_explain_variable_comparison():
    x = 10
    y = 20
    try:
        assert x == y
    except AssertionError:
        import sys
        result = _explain_assertion(sys.exc_info()[2])
        assert result is not None
        assert "10 == 20" in result


def test_explain_non_assert_returns_none():
    result = _explain_assertion(None)
    assert result is None

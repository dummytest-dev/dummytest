"""Tests for _dummytest.assertions and dummytest.asserts."""

from _dummytest.assertions import _Fail, _fail
from dummytest import asserts


def test_fail_raises():
    try:
        _fail("boom")
        assert False, "should have raised"
    except _Fail as e:
        assert str(e) == "boom"


def test_fail_is_assertion_error():
    try:
        _fail()
    except AssertionError:
        pass


def test_assert_equal_pass():
    asserts.assert_equal(1, 1)


def test_assert_equal_fail():
    try:
        asserts.assert_equal(1, 2)
        assert False
    except AssertionError as e:
        assert "1 != 2" in str(e)


def test_assert_not_equal():
    asserts.assert_not_equal(1, 2)


def test_assert_true():
    asserts.assert_true(True)


def test_assert_false():
    asserts.assert_false(False)


def test_assert_is():
    x = object()
    asserts.assert_is(x, x)


def test_assert_is_not():
    asserts.assert_is_not(object(), object())


def test_assert_is_none():
    asserts.assert_is_none(None)


def test_assert_is_not_none():
    asserts.assert_is_not_none(42)


def test_assert_in():
    asserts.assert_in(1, [1, 2, 3])


def test_assert_not_in():
    asserts.assert_not_in(4, [1, 2, 3])


def test_assert_is_instance():
    asserts.assert_is_instance(42, int)


def test_assert_not_is_instance():
    asserts.assert_not_is_instance("hi", int)


def test_assert_raises_context_manager():
    with asserts.assert_raises(ValueError):
        raise ValueError("oops")


def test_assert_raises_callable():
    def boom():
        raise TypeError("nope")
    asserts.assert_raises(TypeError, boom)


def test_assert_raises_fails_when_no_exception():
    try:
        with asserts.assert_raises(ValueError):
            pass
        assert False
    except AssertionError:
        pass

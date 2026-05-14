"""Tests for _dummytest.assertions and dummytest.asserts."""

from _dummytest.assertions import _Fail, _fail
from dummytest import asserts


# --- __doc__ tests ---

def test_module_has_doc():
    assert asserts.__doc__ is not None


def test_assert_equal_has_doc():
    assert asserts.assert_equal.__doc__ is not None


def test_assert_not_equal_has_doc():
    assert asserts.assert_not_equal.__doc__ is not None


def test_assert_true_has_doc():
    assert asserts.assert_true.__doc__ is not None


def test_assert_false_has_doc():
    assert asserts.assert_false.__doc__ is not None


def test_assert_is_has_doc():
    assert asserts.assert_is.__doc__ is not None


def test_assert_is_not_has_doc():
    assert asserts.assert_is_not.__doc__ is not None


def test_assert_is_none_has_doc():
    assert asserts.assert_is_none.__doc__ is not None


def test_assert_is_not_none_has_doc():
    assert asserts.assert_is_not_none.__doc__ is not None


def test_assert_in_has_doc():
    assert asserts.assert_in.__doc__ is not None


def test_assert_not_in_has_doc():
    assert asserts.assert_not_in.__doc__ is not None


def test_assert_is_instance_has_doc():
    assert asserts.assert_is_instance.__doc__ is not None


def test_assert_not_is_instance_has_doc():
    assert asserts.assert_not_is_instance.__doc__ is not None


def test_assert_raises_has_doc():
    assert asserts.assert_raises.__doc__ is not None


# --- _fail tests ---

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


def test_fail_no_message():
    try:
        _fail()
    except _Fail as e:
        assert str(e) == "None"


# --- assert_equal ---

def test_assert_equal_pass():
    asserts.assert_equal(1, 1)


def test_assert_equal_fail():
    try:
        asserts.assert_equal(1, 2)
        assert False
    except AssertionError as e:
        assert "1 != 2" in str(e)


def test_assert_equal_custom_msg():
    try:
        asserts.assert_equal(1, 2, msg="custom")
        assert False
    except AssertionError as e:
        assert str(e) == "custom"


# --- assert_not_equal ---

def test_assert_not_equal_pass():
    asserts.assert_not_equal(1, 2)


def test_assert_not_equal_fail():
    try:
        asserts.assert_not_equal(1, 1)
        assert False
    except AssertionError as e:
        assert "1 == 1" in str(e)


# --- assert_true / assert_false ---

def test_assert_true_pass():
    asserts.assert_true(True)


def test_assert_true_fail():
    try:
        asserts.assert_true(False)
        assert False
    except AssertionError as e:
        assert "Expected True" in str(e)


def test_assert_false_pass():
    asserts.assert_false(False)


def test_assert_false_fail():
    try:
        asserts.assert_false(True)
        assert False
    except AssertionError as e:
        assert "Expected False" in str(e)


# --- assert_is / assert_is_not ---

def test_assert_is_pass():
    x = object()
    asserts.assert_is(x, x)


def test_assert_is_fail():
    try:
        asserts.assert_is(object(), object())
        assert False
    except AssertionError:
        pass


def test_assert_is_not_pass():
    asserts.assert_is_not(object(), object())


def test_assert_is_not_fail():
    x = object()
    try:
        asserts.assert_is_not(x, x)
        assert False
    except AssertionError:
        pass


# --- assert_is_none / assert_is_not_none ---

def test_assert_is_none_pass():
    asserts.assert_is_none(None)


def test_assert_is_none_fail():
    try:
        asserts.assert_is_none(42)
        assert False
    except AssertionError as e:
        assert "Expected None" in str(e)


def test_assert_is_not_none_pass():
    asserts.assert_is_not_none(42)


def test_assert_is_not_none_fail():
    try:
        asserts.assert_is_not_none(None)
        assert False
    except AssertionError as e:
        assert "Expected not None" in str(e)


# --- assert_in / assert_not_in ---

def test_assert_in_pass():
    asserts.assert_in(1, [1, 2, 3])


def test_assert_in_fail():
    try:
        asserts.assert_in(4, [1, 2, 3])
        assert False
    except AssertionError as e:
        assert "not in" in str(e)


def test_assert_not_in_pass():
    asserts.assert_not_in(4, [1, 2, 3])


def test_assert_not_in_fail():
    try:
        asserts.assert_not_in(1, [1, 2, 3])
        assert False
    except AssertionError as e:
        assert "in" in str(e)


# --- assert_is_instance / assert_not_is_instance ---

def test_assert_is_instance_pass():
    asserts.assert_is_instance(42, int)


def test_assert_is_instance_fail():
    try:
        asserts.assert_is_instance("hi", int)
        assert False
    except AssertionError as e:
        assert "not instance" in str(e)


def test_assert_not_is_instance_pass():
    asserts.assert_not_is_instance("hi", int)


def test_assert_not_is_instance_fail():
    try:
        asserts.assert_not_is_instance(42, int)
        assert False
    except AssertionError as e:
        assert "is instance" in str(e)


# --- assert_raises ---

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


def test_assert_raises_callable_no_exception():
    try:
        asserts.assert_raises(ValueError, lambda: None)
        assert False
    except AssertionError:
        pass


def test_assert_raises_wrong_exception():
    try:
        with asserts.assert_raises(ValueError):
            raise TypeError("wrong")
        assert False
    except TypeError:
        pass


def test_assert_raises_with_args():
    def divide(a, b):
        return a / b
    asserts.assert_raises(ZeroDivisionError, divide, 1, 0)

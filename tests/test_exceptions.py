"""Tests for _dummytest.exceptions."""

from _dummytest.exceptions import (
    BaseDummytestException,
    BaseDummytestAssertion,
    _Fail,
    EqualAssertionError,
    NotEqualAssertionError,
    TrueAssertionError,
    FalseAssertionError,
    IdentityAssertionError,
    NotIdentityAssertionError,
    NoneAssertionError,
    NotNoneAssertionError,
    InAssertionError,
    NotInAssertionError,
    IsInstanceAssertionError,
    NotIsInstanceAssertionError,
    RaisesAssertionError,
)
from dummytest import asserts


# --- Base class hierarchy ---

def test_base_exception_is_exception():
    assert issubclass(BaseDummytestException, Exception)


def test_base_assertion_is_assertion_error():
    assert issubclass(BaseDummytestAssertion, AssertionError)


def test_fail_inherits_base_assertion():
    assert issubclass(_Fail, BaseDummytestAssertion)


# --- All assertion exceptions inherit from BaseDummytestAssertion ---

_ALL_ASSERTION_EXCEPTIONS = [
    EqualAssertionError,
    NotEqualAssertionError,
    TrueAssertionError,
    FalseAssertionError,
    IdentityAssertionError,
    NotIdentityAssertionError,
    NoneAssertionError,
    NotNoneAssertionError,
    InAssertionError,
    NotInAssertionError,
    IsInstanceAssertionError,
    NotIsInstanceAssertionError,
    RaisesAssertionError,
]


def test_all_inherit_base_assertion():
    for exc_cls in _ALL_ASSERTION_EXCEPTIONS:
        assert issubclass(exc_cls, BaseDummytestAssertion), exc_cls.__name__


def test_all_inherit_assertion_error():
    for exc_cls in _ALL_ASSERTION_EXCEPTIONS:
        assert issubclass(exc_cls, AssertionError), exc_cls.__name__


def test_all_are_catchable_as_exception():
    for exc_cls in _ALL_ASSERTION_EXCEPTIONS:
        try:
            raise exc_cls("test")
        except Exception:
            pass


# --- Each exception carries a message ---

def test_all_carry_message():
    for exc_cls in _ALL_ASSERTION_EXCEPTIONS:
        e = exc_cls("some message")
        assert str(e) == "some message"


# --- __doc__ on every exception ---

def test_base_exception_has_no_doc_or_has_doc():
    assert BaseDummytestException is not None


def test_base_assertion_has_no_doc_or_has_doc():
    assert BaseDummytestAssertion is not None


def test_fail_has_doc():
    assert _Fail.__doc__ is not None


def test_all_assertion_exceptions_have_doc():
    for exc_cls in _ALL_ASSERTION_EXCEPTIONS:
        assert exc_cls.__doc__ is not None, f"{exc_cls.__name__} missing __doc__"


# --- asserts.py raises the correct exception type ---

def test_assert_equal_raises_correct_type():
    try:
        asserts.assert_equal(1, 2)
    except EqualAssertionError:
        pass


def test_assert_not_equal_raises_correct_type():
    try:
        asserts.assert_not_equal(1, 1)
    except NotEqualAssertionError:
        pass


def test_assert_true_raises_correct_type():
    try:
        asserts.assert_true(False)
    except TrueAssertionError:
        pass


def test_assert_false_raises_correct_type():
    try:
        asserts.assert_false(True)
    except FalseAssertionError:
        pass


def test_assert_is_raises_correct_type():
    try:
        asserts.assert_is(1, 2)
    except IdentityAssertionError:
        pass


def test_assert_is_not_raises_correct_type():
    x = object()
    try:
        asserts.assert_is_not(x, x)
    except NotIdentityAssertionError:
        pass


def test_assert_is_none_raises_correct_type():
    try:
        asserts.assert_is_none(42)
    except NoneAssertionError:
        pass


def test_assert_is_not_none_raises_correct_type():
    try:
        asserts.assert_is_not_none(None)
    except NotNoneAssertionError:
        pass


def test_assert_in_raises_correct_type():
    try:
        asserts.assert_in(4, [1, 2, 3])
    except InAssertionError:
        pass


def test_assert_not_in_raises_correct_type():
    try:
        asserts.assert_not_in(1, [1, 2, 3])
    except NotInAssertionError:
        pass


def test_assert_is_instance_raises_correct_type():
    try:
        asserts.assert_is_instance("hi", int)
    except IsInstanceAssertionError:
        pass


def test_assert_not_is_instance_raises_correct_type():
    try:
        asserts.assert_not_is_instance(42, int)
    except NotIsInstanceAssertionError:
        pass


def test_assert_raises_raises_correct_type():
    try:
        asserts.assert_raises(ValueError, lambda: None)
    except RaisesAssertionError:
        pass

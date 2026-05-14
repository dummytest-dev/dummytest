"""Exceptions for the all module."""


class BaseDummytestException(Exception):
    """Base exception for all dummytest errors."""


class BaseDummytestAssertion(AssertionError):
    """Base class for all dummytest assertion failures."""


class _Fail(BaseDummytestAssertion):
    """Raised by `_fail` to mark a test as explicitly failed."""


class EqualAssertionError(BaseDummytestAssertion):
    """Raised when two values are unexpectedly not equal."""


class NotEqualAssertionError(BaseDummytestAssertion):
    """Raised when two values are unexpectedly equal."""


class TrueAssertionError(BaseDummytestAssertion):
    """Raised when an expression is unexpectedly falsy."""


class FalseAssertionError(BaseDummytestAssertion):
    """Raised when an expression is unexpectedly truthy."""


class IdentityAssertionError(BaseDummytestAssertion):
    """Raised when two objects are unexpectedly not identical."""


class NotIdentityAssertionError(BaseDummytestAssertion):
    """Raised when two objects are unexpectedly identical."""


class NoneAssertionError(BaseDummytestAssertion):
    """Raised when a value is unexpectedly not None."""


class NotNoneAssertionError(BaseDummytestAssertion):
    """Raised when a value is unexpectedly None."""


class InAssertionError(BaseDummytestAssertion):
    """Raised when an item is unexpectedly not in a container."""


class NotInAssertionError(BaseDummytestAssertion):
    """Raised when an item is unexpectedly in a container."""


class IsInstanceAssertionError(BaseDummytestAssertion):
    """Raised when an object is unexpectedly not an instance of a class."""


class NotIsInstanceAssertionError(BaseDummytestAssertion):
    """Raised when an object is unexpectedly an instance of a class."""


class RaisesAssertionError(BaseDummytestAssertion):
    """Raised when an expected exception was not raised."""

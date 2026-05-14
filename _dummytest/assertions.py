"""Assertion helpers for dummytest."""

from .exceptions import _Fail


def _fail(msg=None):
    """
    Explicitly fail the current test.
    """
    # Equivalent to ``unittest.TestCase.fail``. Raises ``_Fail`` (a subclass of
    # ``AssertionError``) with an optional human-readable ``msg``.
    raise _Fail(msg)

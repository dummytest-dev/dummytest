"""Assertion helpers for dummytest."""


class _Fail(AssertionError):
    """Raised by `_fail` to mark a test as explicitly failed."""


def _fail(msg=None):
    """Explicitly fail the current test.

    Equivalent to ``unittest.TestCase.fail``. Raises ``_Fail`` (a subclass of
    ``AssertionError``) with an optional human-readable ``msg``.
    """
    raise _Fail(msg)

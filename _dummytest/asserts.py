"""Assert functions like unittest.

Provides assertion helpers that raise ``AssertionError`` with descriptive
messages on failure. Each function accepts an optional *msg* argument to
override the default message.

Usage::

    from dummytest import asserts

    asserts.assert_equal(1, 1)
    asserts.assert_in("a", ["a", "b"])

    with asserts.assert_raises(ValueError):
        int("not a number")
"""


def assert_equal(a, b, msg=None):
    """Assert ``a == b``."""
    if a != b:
        raise AssertionError(msg or f"{a} != {b}")


def assert_not_equal(a, b, msg=None):
    """Assert ``a != b``."""
    if a == b:
        raise AssertionError(msg or f"{a} == {b}")


def assert_true(expr, msg=None):
    """Assert ``bool(expr)`` is ``True``."""
    if not expr:
        raise AssertionError(msg or "Expected True")


def assert_false(expr, msg=None):
    """Assert ``bool(expr)`` is ``False``."""
    if expr:
        raise AssertionError(msg or "Expected False")


def assert_is(a, b, msg=None):
    """Assert ``a is b``."""
    if a is not b:
        raise AssertionError(msg or f"{a} is not {b}")


def assert_is_not(a, b, msg=None):
    """Assert ``a is not b``."""
    if a is b:
        raise AssertionError(msg or f"{a} is {b}")


def assert_is_none(expr, msg=None):
    """Assert ``expr is None``."""
    if expr is not None:
        raise AssertionError(msg or "Expected None")


def assert_is_not_none(expr, msg=None):
    """Assert ``expr is not None``."""
    if expr is None:
        raise AssertionError(msg or "Expected not None")


def assert_in(item, container, msg=None):
    """Assert ``item in container``."""
    if item not in container:
        raise AssertionError(msg or f"{item} not in {container}")


def assert_not_in(item, container, msg=None):
    """Assert ``item not in container``."""
    if item in container:
        raise AssertionError(msg or f"{item} in {container}")


def assert_is_instance(obj, cls, msg=None):
    """Assert ``isinstance(obj, cls)``."""
    if not isinstance(obj, cls):
        raise AssertionError(msg or f"{obj} is not instance of {cls}")


def assert_not_is_instance(obj, cls, msg=None):
    """Assert ``not isinstance(obj, cls)``."""
    if isinstance(obj, cls):
        raise AssertionError(msg or f"{obj} is instance of {cls}")


def assert_raises(exc_type, func=None, *args, **kwargs):
    """Assert that *exc_type* is raised.

    Can be used as a context manager or by passing a callable::

        with assert_raises(ValueError):
            int("x")

        assert_raises(TypeError, some_func, arg1, arg2)
    """
    class _RaisesContext:
        def __enter__(self):
            return self
        def __exit__(self, exc_tp, exc_val, tb):
            if exc_tp is None:
                raise AssertionError(f"Expected exception {exc_type}")
            if not issubclass(exc_tp, exc_type):
                return False
            return True
    if func is None:
        return _RaisesContext()
    try:
        func(*args, **kwargs)
    except exc_type:
        return
    raise AssertionError(f"Expected exception {exc_type}")

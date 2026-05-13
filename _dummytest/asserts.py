"""Assert functions like unittest."""

def assert_equal(a, b, msg=None):
    if a != b:
        raise AssertionError(msg or f"{a} != {b}")

def assert_not_equal(a, b, msg=None):
    if a == b:
        raise AssertionError(msg or f"{a} == {b}")

def assert_true(expr, msg=None):
    if not expr:
        raise AssertionError(msg or "Expected True")

def assert_false(expr, msg=None):
    if expr:
        raise AssertionError(msg or "Expected False")

def assert_is(a, b, msg=None):
    if a is not b:
        raise AssertionError(msg or f"{a} is not {b}")

def assert_is_not(a, b, msg=None):
    if a is b:
        raise AssertionError(msg or f"{a} is {b}")

def assert_is_none(expr, msg=None):
    if expr is not None:
        raise AssertionError(msg or "Expected None")

def assert_is_not_none(expr, msg=None):
    if expr is None:
        raise AssertionError(msg or "Expected not None")

def assert_in(item, container, msg=None):
    if item not in container:
        raise AssertionError(msg or f"{item} not in {container}")

def assert_not_in(item, container, msg=None):
    if item in container:
        raise AssertionError(msg or f"{item} in {container}")

def assert_is_instance(obj, cls, msg=None):
    if not isinstance(obj, cls):
        raise AssertionError(msg or f"{obj} is not instance of {cls}")

def assert_not_is_instance(obj, cls, msg=None):
    if isinstance(obj, cls):
        raise AssertionError(msg or f"{obj} is instance of {cls}")

def assert_raises(exc_type, func=None, *args, **kwargs):
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
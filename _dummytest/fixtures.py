"""Fixture system for dummytest.

Provides a pytest-like fixture mechanism with dependency injection,
scoped caching, and yield-based teardown.

Usage::

    import dummytest

    @dummytest.fixture
    def db_connection():
        conn = create_connection()
        yield conn
        conn.close()

    @dummytest.fixture(scope="session")
    def app_config():
        return load_config()

    def test_query(db_connection):
        result = db_connection.execute("SELECT 1")
        assert result is not None

Built-in fixtures: ``tmp_path``, ``capsys``, ``monkeypatch``.
"""

import inspect
import io
import os
import pathlib
import shutil
import sys
import tempfile


class FixtureDef:
    """Metadata for a single registered fixture."""

    __slots__ = ("func", "name", "scope", "is_generator")

    def __init__(self, func, scope="function"):
        self.func = func
        self.name = func.__name__
        self.scope = scope
        self.is_generator = inspect.isgeneratorfunction(func)


class FixtureRegistry:
    """Central registry that stores, resolves, and caches fixtures."""

    def __init__(self):
        self._fixtures = {}
        self._session_cache = {}
        self._module_cache = {}
        self._session_teardowns = []
        self._module_teardowns = []
        self._current_module = None

    def register(self, func, scope="function"):
        """Register a callable as a fixture and return it unchanged."""
        fdef = FixtureDef(func, scope)
        self._fixtures[fdef.name] = fdef
        func._dummytest_fixture = True
        return func

    def resolve_params(self, param_names):
        """Resolve a list of parameter names to ``(kwargs, teardowns)``."""
        kwargs = {}
        teardowns = []
        for name in param_names:
            if name not in self._fixtures:
                available = ", ".join(sorted(self._fixtures.keys()))
                raise LookupError(
                    f"Fixture '{name}' not found. Available: [{available}]"
                )
            value, td = self._resolve_one(name)
            kwargs[name] = value
            if td:
                teardowns.append(td)
        return kwargs, teardowns

    def _resolve_one(self, name):
        fdef = self._fixtures[name]

        if fdef.scope == "session" and name in self._session_cache:
            return self._session_cache[name], None
        if fdef.scope == "module" and name in self._module_cache:
            return self._module_cache[name], None

        dep_names = [
            p for p in inspect.signature(fdef.func).parameters
            if p != "self"
        ]
        dep_kwargs, dep_teardowns = self.resolve_params(dep_names) if dep_names else ({}, [])

        if fdef.is_generator:
            gen = fdef.func(**dep_kwargs)
            value = next(gen)

            def teardown():
                try:
                    next(gen)
                except StopIteration:
                    pass
                for td in reversed(dep_teardowns):
                    td()
        else:
            value = fdef.func(**dep_kwargs)

            def teardown():
                for td in reversed(dep_teardowns):
                    td()
            if not dep_teardowns:
                teardown = None

        if fdef.scope == "session":
            self._session_cache[name] = value
            if teardown:
                self._session_teardowns.append(teardown)
            return value, None
        elif fdef.scope == "module":
            self._module_cache[name] = value
            if teardown:
                self._module_teardowns.append(teardown)
            return value, None
        else:
            return value, teardown

    def start_session(self):
        """Clear all caches. Call once before the test loop."""
        self._session_cache.clear()
        self._module_cache.clear()
        self._session_teardowns.clear()
        self._module_teardowns.clear()
        self._current_module = None

    def set_module(self, module_name):
        """Track current module; teardown module-scoped fixtures on change."""
        if module_name != self._current_module:
            self._teardown_module()
            self._current_module = module_name

    def _teardown_module(self):
        for td in reversed(self._module_teardowns):
            try:
                td()
            except Exception:
                pass
        self._module_cache.clear()
        self._module_teardowns.clear()

    def teardown_session(self):
        """Teardown all module and session-scoped fixtures."""
        self._teardown_module()
        for td in reversed(self._session_teardowns):
            try:
                td()
            except Exception:
                pass
        self._session_cache.clear()
        self._session_teardowns.clear()


_registry = FixtureRegistry()


def fixture(func=None, *, scope="function"):
    """Mark a function as a dummytest fixture.

    Can be used with or without parentheses::

        @dummytest.fixture
        def my_fixture():
            return 42

        @dummytest.fixture(scope="session")
        def shared_resource():
            r = acquire()
            yield r
            release(r)

    Scopes: ``"function"`` (default), ``"module"``, ``"session"``.
    """
    if func is not None:
        return _registry.register(func, scope="function")

    def decorator(fn):
        return _registry.register(fn, scope=scope)
    return decorator


# --- Built-in fixtures ---

@fixture
def tmp_path():
    """Provide a temporary directory as a ``pathlib.Path``, removed after the test."""
    d = pathlib.Path(tempfile.mkdtemp())
    yield d
    shutil.rmtree(d, ignore_errors=True)


class _CaptureResult:
    """Captured stdout/stderr returned by the ``capsys`` fixture."""

    def __init__(self):
        self._out = io.StringIO()
        self._err = io.StringIO()

    def readouterr(self):
        """Return ``(out, err)`` strings and reset the capture buffers."""
        out = self._out.getvalue()
        err = self._err.getvalue()
        self._out.truncate(0)
        self._out.seek(0)
        self._err.truncate(0)
        self._err.seek(0)
        return out, err


@fixture
def capsys():
    """Capture writes to ``sys.stdout`` and ``sys.stderr``.

    Use ``capsys.readouterr()`` to get ``(out, err)`` strings.
    """
    cap = _CaptureResult()
    old_out, old_err = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = cap._out, cap._err
    yield cap
    sys.stdout, sys.stderr = old_out, old_err


class _MonkeyPatch:
    """Patch objects, dicts, and environment variables for the duration of a test."""

    def __init__(self):
        self._undos = []

    def setattr(self, obj, name, value):
        """Set an attribute on *obj*, restored after the test."""
        old = getattr(obj, name, _NOTSET)
        if old is _NOTSET:
            self._undos.append(lambda: delattr(obj, name))
        else:
            self._undos.append(lambda: setattr(obj, name, old))
        setattr(obj, name, value)

    def delattr(self, obj, name):
        """Delete an attribute on *obj*, restored after the test."""
        old = getattr(obj, name)
        self._undos.append(lambda: setattr(obj, name, old))
        delattr(obj, name)

    def setenv(self, name, value):
        """Set an environment variable, restored after the test."""
        old = os.environ.get(name, _NOTSET)
        if old is _NOTSET:
            self._undos.append(lambda: os.environ.pop(name, None))
        else:
            self._undos.append(lambda: os.environ.__setitem__(name, old))
        os.environ[name] = value

    def delenv(self, name, raising=True):
        """Delete an environment variable, restored after the test."""
        old = os.environ.get(name, _NOTSET)
        if old is _NOTSET:
            if raising:
                raise KeyError(name)
            return
        self._undos.append(lambda: os.environ.__setitem__(name, old))
        del os.environ[name]

    def undo(self):
        """Revert all patches in reverse order."""
        for fn in reversed(self._undos):
            fn()
        self._undos.clear()


_NOTSET = object()


@fixture
def monkeypatch():
    """Patch objects, dicts, and environment variables for the duration of a test.

    Methods: ``setattr``, ``delattr``, ``setenv``, ``delenv``.
    """
    mp = _MonkeyPatch()
    yield mp
    mp.undo()

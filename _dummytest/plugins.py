"""Built-in plugins for dummytest.

While the runner is active, these names are injected into ``builtins`` so test
code can call them without importing or qualifying with ``dummytest.``::

    import dummytest

    def test_x():
        x = compute()
        if dummytest.PLUGINABLE:
            reveal_type(x)
            dump_locals()
        assert x == 42

The ``if dummytest.PLUGINABLE:`` guard keeps the bare names safe to leave in
test sources: outside the runner ``PLUGINABLE`` is ``False`` so the guarded
block never executes (and the bare names are not bound).
"""

import builtins
import functools
import sys

from .const import _set_pluggable
from .color import c as _c


def reveal_type(value):
    """Print the runtime type of ``value`` and return it unchanged.

    Dummytest analogue of mypy's ``reveal_type``: where mypy reports the
    statically inferred type at type-check time, this reports the runtime type
    while tests are executing.
    """
    print(_c.bold_blue(f"reveal_type | {type(value).__name__} = {value!r}"))
    return value


def dump_locals():
    """Print the caller's local variables, one per line."""
    frame = sys._getframe(1)
    qualname = getattr(frame.f_code, "co_qualname", frame.f_code.co_name)
    print(_c.bold_blue(f"dump_locals | {qualname}"))
    for name, val in frame.f_locals.items():
        if name.startswith("__"):
            continue
        print(f"  {name} = {val!r}")


def record_calls(func):
    """Wrap ``func`` so each call is printed with arguments and result."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        argstr = ", ".join(
            [repr(a) for a in args]
            + [f"{k}={v!r}" for k, v in kwargs.items()]
        )
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(_c.bold_blue(f"record_calls | {func.__name__}({argstr}) raised {type(e).__name__}"))
            raise
        print(_c.bold_blue(f"record_calls | {func.__name__}({argstr}) -> {result!r}"))
        return result
    return wrapper


_PLUGIN_NAMES = ("reveal_type", "dump_locals", "record_calls")


def _install_plugins():
    _set_pluggable(True)
    for name in _PLUGIN_NAMES:
        setattr(builtins, name, globals()[name])


def _uninstall_plugins():
    for name in _PLUGIN_NAMES:
        if hasattr(builtins, name):
            delattr(builtins, name)
    _set_pluggable(False)

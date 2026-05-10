"""Const for errortest module."""


class _PluggableState:
    """Toggle exposed as ``PLUGINABLE``.

    Behaves like ``typing.TYPE_CHECKING``: ``False`` at import time, but flipped
    to ``True`` while the dummytest runner is executing tests. Plugin code (e.g.
    a call to ``reveal_type``) should be guarded by ``if PLUGINABLE:`` so it
    only runs under the test runner.
    """

    enabled = False

    def __bool__(self):
        return type(self).enabled

    def __repr__(self):
        return f"PLUGINABLE({type(self).enabled})"


PLUGINABLE = _PluggableState()


def _set_pluggable(value):
    _PluggableState.enabled = bool(value)

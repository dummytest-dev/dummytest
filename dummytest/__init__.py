"""dummytest: Plugins, fixtures, workflows, unit and functional tests with Python."""

from _dummytest._version import (__version__,
                                __version_tuple__,
                                __commit_id__)
from _dummytest.const import (PLUGINABIE)
from _dummytest.assertions import _fail as fail

__all__ = [
    "__version__",
    "__version_tuple__",
    "__commit_id__",
    "PLUGINABIE",
    "fail"
]
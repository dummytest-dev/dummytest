"""dummytest: Plugins, fixtures, workflows, unit and functional tests with Python."""

from _dummytest._version import (__version__,
                                __version_tuple__,
                                __commit_id__)
from _dummytest.const import PLUGINABLE
from _dummytest.assertions import _fail as fail
from _dummytest.fixtures import fixture
from _dummytest.plugins import reveal_type, dump_locals, record_calls
from _dummytest import asserts

__all__ = [
    "__version__",
    "__version_tuple__",
    "__commit_id__",
    "PLUGINABLE",
    "fail",
    "fixture",
    "reveal_type",
    "dump_locals",
    "record_calls",
    "asserts"
]
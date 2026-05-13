"""Shared fixtures and helpers for the dummytest test suite."""

import sys
import pathlib

ROOT = pathlib.Path(__file__).parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import dummytest


@dummytest.fixture
def sample_list():
    return [1, 2, 3]


@dummytest.fixture
def sample_dict():
    return {"a": 1, "b": 2}

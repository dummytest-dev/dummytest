"""Shared fixtures and helpers for the dummytest test suite."""

import sys

# ---------------------------------------------------------------------------
# Ensure the project root (contains both `dummytest/` and `_dummytest/`)
# is on sys.path so that `import dummytest` and `from _dummytest import …`
# both resolve correctly when running dummytest from any directory.
# ---------------------------------------------------------------------------
import pathlib

ROOT = pathlib.Path(__file__).parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
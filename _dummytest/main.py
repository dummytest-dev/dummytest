"""Core implementation of the testing process for dummytest."""


import sys

from .run import _run_exception_test_suite


def main():
    _run_exception_test_suite()
    sys.exit(0)
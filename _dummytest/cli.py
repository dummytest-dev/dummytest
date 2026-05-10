"""Core implementation of the cli for dummytest."""

import argparse

from ._version import __version__


def _cli_parser():
    temp_parser = argparse.ArgumentParser(add_help=False)
    temp_parser.add_argument("--no-color", action="store_true")
    args_partial, _ = temp_parser.parse_known_args()

    use_color = not args_partial.no_color

    parser = argparse.ArgumentParser(
        prog="dummytest",
        description="dummytest: Plugins, fixtures, workflows, unit and functional tests with Python.",
        color=use_color
    )

    parser.add_argument(
        "--config", "-c",
        help="The config file."
    )    

    parser.add_argument(
        "--version",
        action="version",
        version=f"dummytest {__version__}",
        help="Show version and exit."
    )

    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Suppress colored output."
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print full traceback for failing tests."
    )

    parser.add_argument(
        "--test-dir",
        help="Specify test directory (default: tests)"
    )

    parser.add_argument(
        "--test-file",
        help="Specify test file"
    )

    parser.add_argument(
        "--test-pattern",
        help="Glob pattern for test files in --test-dir (default: test_*.py)"
    )

    parser.add_argument(
        "expr",
        nargs="?",
        help="Inline Python statement(s) to run as a single test, e.g. 'assert 1+1==2'."
    )

    args = parser.parse_args()

    if not args.config:
        args.config = "dummytest.ini"

    return args

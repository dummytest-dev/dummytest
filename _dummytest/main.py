"""Core implementation of the testing process for dummytest."""


import sys

from .config.config import _read_bool_config, _read_str_config, init_config
from .cli import _cli_parser
from .run import _run_test_suite


def main():
    args = _cli_parser()

    init_config(args.config)

    args.no_color = args.no_color or _read_bool_config("no_color")

    test_file = args.test_file or _read_str_config("test_file")
    test_dir = args.test_dir or _read_str_config("test_dir")

    args.test_target = test_file if test_file else test_dir

    _run_test_suite(args)

    sys.exit(0)
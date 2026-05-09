"""Core implementation of the testing process for dummytest."""


import sys

from .config.config import _read_bool_config, init_config
from .cli import _cli_parser
from .run import _run_test_suite


def main():
    args = _cli_parser()

    init_config(args.config)

    config_no_color = _read_bool_config("no_color")
    cli_no_color = args.no_color
    final_no_color = cli_no_color or config_no_color

    args.no_color = final_no_color
    
    _run_test_suite(args)

    sys.exit(0)
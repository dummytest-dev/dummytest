"""Core implementation of the testing process for dummytest."""


import sys

from .config.config import _read_bool_config, _read_str_config, init_config
from .config.toml import _read_toml_config, _init_toml_config
from .cli import _cli_parser
from .ignores import load_ignore_rules
from .run import _run_inline, _run_test_suite
from .warnings import _check_version_warnings


_IGNORE_FILE = ".dummytestignore"


def main():
    _check_version_warnings()
    args = _cli_parser()

    init_config(args.config)
    _init_toml_config()

    args.no_color = args.no_color or _read_bool_config("no_color") or _read_toml_config("no_color")
    args.verbose = args.verbose or _read_bool_config("verbose") or _read_toml_config("verbose")
    args.ignore_rules = load_ignore_rules(_IGNORE_FILE)

    if args.expr:
        _run_inline(args)
        sys.exit(0)

    test_file = args.test_file or _read_str_config("test_file") or _read_toml_config("test_file")
    test_dir = args.test_dir or _read_str_config("test_dir") or _read_toml_config("test_dir")

    args.test_target = test_file if test_file else test_dir
    args.test_pattern = args.test_pattern or _read_str_config("test_pattern") or _read_toml_config("test_pattern")

    _run_test_suite(args)

    sys.exit(0)
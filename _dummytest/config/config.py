"""Read ini config files."""

import pathlib
import configparser as cp


_config = cp.ConfigParser()
_CWD = pathlib.Path.cwd()
_DEFAULT_CONFIG_FILE = "dummytest.ini"
_SECTION = "dummytest"

_CONFIG_DEFAULTS = {
    "no_color": {"type": bool, "default": False},
    "verbose": {"type": bool, "default": False},
    "test_dir": {"type": str, "default": "tests"},
    "test_file": {"type": str, "default": ""},
    "test_pattern": {"type": str, "default": "test_*.py"}
}


def init_config(config_path=None):
    if not config_path:
        config_path = _CWD / _DEFAULT_CONFIG_FILE
    else:
        config_path = _CWD / config_path
    _config.read(config_path)



def _read_bool_config(name):
    try:
        return _config.getboolean(_SECTION, name)
    except (cp.NoSectionError, cp.NoOptionError, ValueError, KeyError):
        return _CONFIG_DEFAULTS[name]["default"]


def _read_int_config(name):
    try:
        return _config.getint(_SECTION, name)
    except (cp.NoSectionError, cp.NoOptionError, ValueError, KeyError):
        return _CONFIG_DEFAULTS[name]["default"]


def _read_str_config(name):
    try:
        return _config.get(_SECTION, name)
    except (cp.NoSectionError, cp.NoOptionError, KeyError):
        return _CONFIG_DEFAULTS[name]["default"]
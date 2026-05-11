"""Read config in `pyproject.toml`."""

import pathlib
import tomllib

from .config import _CONFIG_DEFAULTS


_CWD = pathlib.Path.cwd()
_DEFAULT_TOML_FILE = "pyproject.toml"
_SECTION = "tool"
_SUBSECTION = "dummytest"

_toml_config = {}


def _init_toml_config(toml_path=None):
    global _toml_config
    if not toml_path:
        toml_path = _CWD / _DEFAULT_TOML_FILE
    else:
        toml_path = _CWD / toml_path
    try:
        with open(toml_path, "rb") as f:
            data = tomllib.load(f)
        _toml_config = data.get(_SECTION, {}).get(_SUBSECTION, {})
    except (FileNotFoundError, tomllib.TOMLDecodeError):
        _toml_config = {}


def _read_toml_config(name):
    value = _toml_config.get(name)
    if value is not None and isinstance(value, _CONFIG_DEFAULTS[name]["type"]):
        return value
    return _CONFIG_DEFAULTS[name]["default"]

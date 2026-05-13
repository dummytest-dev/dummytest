"""Tests for _dummytest.config.toml (pyproject.toml config reading)."""

import pathlib
import tempfile

from _dummytest.config import toml as toml_cfg


def test_init_toml_config_reads_values():
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".toml", delete=False) as f:
        f.write(b'[tool.dummytest]\nno_color = true\nverbose = false\ntest_dir = "toml_tests"\n')
        f.flush()
        toml_path = pathlib.Path(f.name)

    toml_cfg._toml_config = {}
    toml_cfg._init_toml_config(toml_path)

    assert toml_cfg._read_toml_config("no_color") is True
    assert toml_cfg._read_toml_config("verbose") is False
    assert toml_cfg._read_toml_config("test_dir") == "toml_tests"

    toml_path.unlink()


def test_read_toml_config_default():
    toml_cfg._toml_config = {}
    assert toml_cfg._read_toml_config("no_color") is False
    assert toml_cfg._read_toml_config("verbose") is False
    assert toml_cfg._read_toml_config("test_dir") == "tests"


def test_init_toml_config_nonexistent():
    toml_cfg._toml_config = {}
    toml_cfg._init_toml_config("nonexistent_pyproject_abc123.toml")
    assert toml_cfg._read_toml_config("no_color") is False


def test_read_toml_config_wrong_type_returns_default():
    toml_cfg._toml_config = {"no_color": "yes", "test_dir": 123}
    assert toml_cfg._read_toml_config("no_color") is False
    assert toml_cfg._read_toml_config("test_dir") == "tests"

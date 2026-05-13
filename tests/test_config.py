"""Tests for _dummytest.config.config (ini config reading)."""

import pathlib
import tempfile

from _dummytest.config import config as cfg


def test_init_config_reads_ini():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".ini", delete=False) as f:
        f.write("[dummytest]\nno_color = true\nverbose = false\ntest_dir = my_tests\n")
        f.flush()
        ini_path = pathlib.Path(f.name)

    cfg._config = cfg.cp.ConfigParser()
    cfg._config.read(ini_path)

    assert cfg._read_bool_config("no_color") is True
    assert cfg._read_bool_config("verbose") is False
    assert cfg._read_str_config("test_dir") == "my_tests"

    ini_path.unlink()


def test_read_bool_config_default():
    cfg._config = cfg.cp.ConfigParser()
    assert cfg._read_bool_config("no_color") is False
    assert cfg._read_bool_config("verbose") is False


def test_read_str_config_default():
    cfg._config = cfg.cp.ConfigParser()
    assert cfg._read_str_config("test_dir") == "tests"
    assert cfg._read_str_config("test_file") == ""
    assert cfg._read_str_config("test_pattern") == "test_*.py"


def test_init_config_nonexistent_file():
    cfg._config = cfg.cp.ConfigParser()
    cfg.init_config("nonexistent_file_abc123.ini")
    assert cfg._read_bool_config("no_color") is False
    assert cfg._read_str_config("test_dir") == "tests"

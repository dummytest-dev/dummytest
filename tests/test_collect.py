"""Tests for _dummytest.collect and _dummytest.find."""

import pathlib
import tempfile

from _dummytest.collect import _collect_all_test_cases


def test_collect_from_file():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", prefix="test_", delete=False, dir=".") as f:
        f.write("def test_alpha(): pass\ndef test_beta(): pass\ndef helper(): pass\n")
        f.flush()
        test_file = pathlib.Path(f.name)

    cases = _collect_all_test_cases(str(test_file))
    names = [c.__name__ for c in cases]
    assert "test_alpha" in names
    assert "test_beta" in names
    assert "helper" not in names

    test_file.unlink()


def test_collect_from_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        p = pathlib.Path(tmpdir)
        (p / "test_one.py").write_text("def test_x(): pass\n")
        (p / "test_two.py").write_text("def test_y(): pass\n")
        (p / "helper.py").write_text("def test_z(): pass\n")

        cases = _collect_all_test_cases(str(p), "test_*.py")
        names = [c.__name__ for c in cases]
        assert "test_x" in names
        assert "test_y" in names
        assert "test_z" not in names


def test_collect_test_class_methods():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", prefix="test_", delete=False, dir=".") as f:
        f.write("class TestFoo:\n    def test_method(self): pass\n    def helper(self): pass\n")
        f.flush()
        test_file = pathlib.Path(f.name)

    cases = _collect_all_test_cases(str(test_file))
    names = [c.__name__ for c in cases]
    assert "test_method" in names
    assert "helper" not in names

    test_file.unlink()


def test_collect_empty_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        cases = _collect_all_test_cases(str(tmpdir), "test_*.py")
        assert cases == []

"""Collect all: top-level test funcs + test class test methods"""


import importlib.util
import pathlib
import sys

from .find import (
    _find_test_classes,
    _find_test_functions,
    _find_test_methods
)


def _collect_all_test_cases(test_dir):
    test_path = pathlib.Path(test_dir).resolve()
    all_tests = []

    if str(test_path.parent) not in sys.path:
        sys.path.insert(0, str(test_dir.parent))

    for file in test_path.glob("test_*.py"):
        module_name = file.stem

        spec = importlib.util.spec_from_file_location(module_name, file)
        if not spec:
            continue

        mod = importlib.util.module_from_spec(spec)

        if spec.loader is not None:
            spec.loader.exec_module(mod)
        else:
            continue

        all_tests.extend(_find_test_functions(mod))
        for cls in _find_test_classes(mod):
            all_tests.extend(_find_test_methods(cls))

    return all_tests
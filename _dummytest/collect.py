"""Collect all: top-level test funcs + test class test methods"""

import sys

from .find import (
    _find_test_classes,
    _find_test_functions,
    _find_test_methods
)


def _collect_all_test_cases():
    module = sys.modules["__main__"] 
    
    all_tests = []
    all_tests.extend(_find_test_functions(module))
    for cls in _find_test_classes(module):
        all_tests.extend(_find_test_methods(cls))
    return all_tests
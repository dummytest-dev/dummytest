"""Find test functions or classes."""

import inspect
import sys


def _find_test_functions():
    current_module = sys.modules["__main__"]

    all_members = inspect.getmembers(current_module, inspect.isfunction)

    test_functions = []
    for name, func in all_members:
        if name.startswith("test_"):
            test_functions.append(func)

    return test_functions


def _find_test_classes():
    module = sys.modules["__main__"]
    classes = []
    for name, obj in inspect.getmembers(module, inspect.isclass):

        if name.startswith("Test") and obj.__module__ == module.__name__:
            classes.append(obj)
    return classes


def _find_test_methods(test_cls):
    methods = []
    for name, member in inspect.getmembers(test_cls, inspect.isfunction):
        if name.startswith("test_"):
            methods.append(member)
    return methods
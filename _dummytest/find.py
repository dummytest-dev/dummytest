"""Find test functions or classes."""

import inspect


def _find_test_functions(module):
    funcs = []
    for name, obj in inspect.getmembers(module, inspect.isfunction):
        if name.startswith("test_") and obj.__module__ == module.__name__:
            funcs.append(obj)
    return funcs


def _find_test_classes(module):
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
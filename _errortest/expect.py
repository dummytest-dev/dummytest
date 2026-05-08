"""Declare the exception expected to be thrown by the test function."""

def _expect_exception(exception_type):
    def decorator(func):
        func.__expect_exception__ = exception_type
        return func
    return decorator


def _expect_warning(warning_type):
    def decorator(func):
        func.__expect_warning__ = warning_type
        return func
    return decorator

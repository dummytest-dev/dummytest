"""Run tests."""

import linecache
import sys
import traceback

from .assertions import _Fail
from .collect import _collect_all_test_cases
from .explain import _explain_assertion
from .plugins import _install_plugins, _uninstall_plugins


def _run_single_test(test_func):
    func_name = test_func.__qualname__

    try:
        if "." in func_name:
            cls_name = func_name.split(".")[0]
            cls = test_func.__globals__[cls_name]
            test_func(cls())
        else:
            test_func()

        return True, f"PASS | {func_name}", None, None

    except Exception as e:
        reason = "fail by user" if isinstance(e, _Fail) else type(e).__name__
        explain = None
        if isinstance(e, AssertionError) and not isinstance(e, _Fail):
            explain = _explain_assertion(sys.exc_info()[2])
        return False, f"FAIL | {func_name} -> {reason}", traceback.format_exc(), explain


def _print_banner(no_color):
    if no_color:
        print("Dummytest Test Suite Running...")
    else:
        print("\033[1;34mDummytest Test Suite Running...\033[0m")


def _print_result(ok, msg, tb, explain, no_color, verbose):
    if not no_color:
        msg = f"\033[32m{msg}\033[0m" if ok else f"\033[31m{msg}\033[0m"
    print(msg)
    if not ok and explain:
        print(explain)
    if not ok and verbose and tb:
        print(tb, end="")


def _print_summary(total, passed, failed, no_color):
    summary = f"\nTotal: {total} | Passed: {passed} | Failed: {failed}"
    if not no_color:
        if failed == 0:
            summary = f"\033[1;32m{summary}\033[0m"
        else:
            summary = f"\033[1;33m{summary}\033[0m"
    print(summary)


def _run_test_suite(args):
    _print_banner(args.no_color)

    test_cases = _collect_all_test_cases(args.test_target, args.test_pattern)

    total = len(test_cases)
    passed = 0
    failed = 0

    _install_plugins()
    try:
        for case in test_cases:
            ok, msg, tb, explain = _run_single_test(case)
            _print_result(ok, msg, tb, explain, args.no_color, args.verbose)
            if ok:
                passed += 1
            else:
                failed += 1
    finally:
        _uninstall_plugins()

    _print_summary(total, passed, failed, args.no_color)


def _run_inline(args):
    _print_banner(args.no_color)

    src = args.expr
    if not src.endswith("\n"):
        src += "\n"
    filename = "<inline>"
    linecache.cache[filename] = (
        len(src), None, src.splitlines(keepends=True), filename,
    )

    code = compile(src, filename, "exec")
    ns = {"__name__": "__inline__"}

    def _inline():
        exec(code, ns)
    _inline.__qualname__ = "<inline>"

    _install_plugins()
    try:
        ok, msg, tb, explain = _run_single_test(_inline)
    finally:
        _uninstall_plugins()
    _print_result(ok, msg, tb, explain, args.no_color, args.verbose)
    _print_summary(1, 1 if ok else 0, 0 if ok else 1, args.no_color)

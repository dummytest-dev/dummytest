"""Run tests."""

import inspect
import linecache
import sys
import time
import traceback

from .print import _classify, _print_banner, _print_result, _print_summary
from .assertions import _Fail
from .collect import _collect_all_test_cases
from .explain import _explain_assertion
from .plugins import _install_plugins, _uninstall_plugins


def _run_single_test(test_func):
    func_name = test_func.__qualname__
    try:
        source_file = inspect.getsourcefile(test_func) or ""
    except TypeError:
        source_file = ""

    try:
        if "." in func_name:
            cls_name = func_name.split(".")[0]
            cls = test_func.__globals__[cls_name]
            test_func(cls())
        else:
            test_func()

        return {
            "ok": True,
            "label": f"PASS | {func_name}",
            "func_name": func_name,
            "source_file": source_file,
            "exc_name": None,
            "tb": None,
            "explain": None,
        }

    except Exception as e:
        reason = "fail by user" if isinstance(e, _Fail) else type(e).__name__
        explain = None
        if isinstance(e, AssertionError) and not isinstance(e, _Fail):
            explain = _explain_assertion(sys.exc_info()[2])
        return {
            "ok": False,
            "label": f"FAIL | {func_name} -> {reason}",
            "func_name": func_name,
            "source_file": source_file,
            "exc_name": type(e).__name__,
            "tb": traceback.format_exc(),
            "explain": explain,
        }


def _run_test_suite(args):
    _print_banner(args.no_color)
    start = time.perf_counter()

    test_cases = _collect_all_test_cases(args.test_target, args.test_pattern)
    ignore_rules = getattr(args, "ignore_rules", []) or []

    total = len(test_cases)
    passed = 0
    failed = 0
    ignored = 0
    failures = []

    _install_plugins()
    try:
        for i, case in enumerate(test_cases, 1):
            result = _run_single_test(case)
            status, label = _classify(result, ignore_rules)
            _print_result(status, label, result["tb"], result["explain"],
                          args.no_color, args.verbose, index=i, total=total)
            if status == "pass":
                passed += 1
            elif status == "fail":
                failed += 1
                failures.append(result)
            else:
                ignored += 1
    finally:
        _uninstall_plugins()

    elapsed = time.perf_counter() - start
    _print_summary(total, passed, failed, ignored, args.no_color, failures=failures, verbose=args.verbose, elapsed=elapsed)


def _run_inline(args):
    _print_banner(args.no_color)
    start = time.perf_counter()

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

    ignore_rules = getattr(args, "ignore_rules", []) or []

    _install_plugins()
    try:
        result = _run_single_test(_inline)
    finally:
        _uninstall_plugins()

    if not result["ok"]:
        result["source_file"] = filename
    status, label = _classify(result, ignore_rules)
    _print_result(status, label, result["tb"], result["explain"],
                  args.no_color, args.verbose, index=1, total=1)
    passed = 1 if status == "pass" else 0
    failed = 1 if status == "fail" else 0
    ignored = 1 if status == "ignored" else 0
    failures = [result] if status == "fail" else []
    elapsed = time.perf_counter() - start
    _print_summary(1, passed, failed, ignored, args.no_color, failures=failures, verbose=args.verbose, elapsed=elapsed)

"""Run tests."""

from .collect import _collect_all_test_cases


def _run_single_test(test_func):
    func_name = test_func.__qualname__

    try:
        if "." in func_name:
            cls_name = func_name.split(".")[0]
            cls = test_func.__globals__[cls_name]
            test_func(cls())
        else:
            test_func()

        return True, f"PASS | {func_name}"

    except Exception as e:
        return False, f"FAIL | {func_name} -> {type(e).__name__}"


def _run_test_suite(args):
    no_color = args.no_color

    if no_color:
        print("Dummytest Test Suite Running...")
    else:
        print("\033[1;34mDummytest Test Suite Running...\033[0m")

    test_cases = _collect_all_test_cases(args.test_target)

    total = len(test_cases)
    passed = 0
    failed = 0

    for case in test_cases:
        ok, msg = _run_single_test(case)

        if not no_color:
            if ok:
                msg = f"\033[32m{msg}\033[0m" 
            else:
                msg = f"\033[31m{msg}\033[0m"  

        print(msg)

        if ok:
            passed += 1
        else:
            failed += 1

    summary = f"\nTotal: {total} | Passed: {passed} | Failed: {failed}"
    if not no_color:
        if failed == 0:
            summary = f"\033[1;32m{summary}\033[0m"
        else:
            summary = f"\033[1;33m{summary}\033[0m"

    print(summary)

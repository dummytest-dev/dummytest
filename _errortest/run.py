"""Run tests."""

from _errortest.collect import _collect_all_test_cases


def _run_single_test(test_func):
    func_name = test_func.__qualname__

    instance = None
    if "." in func_name:
        cls_name = func_name.split(".")[0]
        cls = test_func.__globals__[cls_name]
        instance = cls()

    try:
        if instance is not None:
            test_func(instance)
        else:
            test_func()
            
        return True, f"PASS | {func_name}"
        
    except Exception as e:
        return False, f"FAIL | {func_name} -> {type(e).__name__}"


def _run_exception_test_suite():
    print("Exception-Focused Test Suite Running...")
    test_cases = _collect_all_test_cases()

    total = len(test_cases)
    passed = 0
    failed = 0

    for case in test_cases:
        ok, msg = _run_single_test(case)
        print(msg)
        if ok:
            passed += 1
        else:
            failed += 1

    print(f"Total: {total} | Passed: {passed} | Failed: {failed}")

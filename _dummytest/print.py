"""Print functions for run.py."""


import sys

from .color import c as _c
from .ignores import is_ignored


def _print_banner(no_color):
    if no_color:
        print("Dummytest Test Suite Running...")
        _print_setup(color=True)
    else:
        print(_c.bold_blue("Dummytest Test Suite Running..."))
        _print_setup(color=False)


def _color_text(text, color_func, no_color):
    if no_color:
        return text
    return color_func(text)


def _print_result(status, label, tb, explain, no_color, verbose):
    if status == "pass":
        label = _color_text(label, _c.green, no_color)
    elif status == "fail":
        label = _color_text(label, _c.red, no_color)
    else:
        label = _color_text(label, _c.yellow, no_color)
    print(label)

    if status != "pass" and explain:
        print(explain)
    if status == "fail" and verbose and tb:
        print(tb, end="")


def _print_summary(total, passed, failed, ignored, no_color):
    parts = [f"Total: {total}", f"Passed: {passed}", f"Failed: {failed}"]
    if ignored:
        parts.append(f"Ignored: {ignored}")
    summary = "\n" + " | ".join(parts)

    if failed == 0:
        summary = _color_text(summary, _c.bold_green, no_color)
    else:
        summary = _color_text(summary, _c.bold_yellow, no_color)
    print(summary)


def _classify(result, ignore_rules):
    if result["ok"]:
        return "pass", result["label"]
    if is_ignored(ignore_rules, result["exc_name"], result["source_file"]):
        label = f"IGNORED | {result['func_name']} -> {result['exc_name']}"
        return "ignored", label
    return "fail", result["label"]


def _print_setup(color):
    ver = '.'.join(map(str, sys.version_info[:3]))
    _s = f"platform: {sys.platform}, python {ver}"
    print(_color_text(_s, _c.cyan, color))
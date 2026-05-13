"""Print functions for run.py."""


import sys

from .color import c as _c
from .ignores import is_ignored
from ._version import __version__


def _supports_unicode():
    try:
        "✓".encode(sys.stdout.encoding or "ascii")
        return True
    except (UnicodeEncodeError, LookupError):
        return False


_UNICODE = _supports_unicode()
_PASS_SYMBOL = "✓" if _UNICODE else "+"
_FAIL_SYMBOL = "✗" if _UNICODE else "x"
_IGNORE_SYMBOL = "⚠" if _UNICODE else "!"
_WARN_SYMBOL = "⚠" if _UNICODE else "!"
_SEPARATOR = "─" if _UNICODE else "-"


def _print_banner(no_color):
    line = _SEPARATOR * 50
    if no_color:
        print(line)
        print("Dummytest Test Suite Running...")
        _print_setup(color=True)
        print(line)
    else:
        print(_c.intense_black(line))
        print(_c.bold_blue("Dummytest Test Suite Running..."))
        _print_setup(color=False)
        print(_c.intense_black(line))


def _color_text(text, color_func, no_color):
    if no_color:
        return text
    return color_func(text)


def _print_result(status, label, tb, explain, no_color, verbose, index=None, total=None):
    progress = ""
    if index is not None and total is not None:
        progress = f"[{index}/{total}] "

    if status == "pass":
        symbol = _PASS_SYMBOL
        line = _color_text(f"  {symbol} {progress}{label}", _c.green, no_color)
    elif status == "fail":
        symbol = _FAIL_SYMBOL
        line = _color_text(f"  {symbol} {progress}{label}", _c.red, no_color)
    else:
        symbol = _IGNORE_SYMBOL
        line = _color_text(f"  {symbol} {progress}{label}", _c.yellow, no_color)
    print(line)

    if status != "pass" and explain:
        print(explain)
    if status == "fail" and verbose and tb:
        print(tb, end="")


def _print_failure_detail(result, no_color):
    source = result.get("source_file", "")
    func = result.get("func_name", "")
    explain = result.get("explain")

    header = _color_text(f"  {_FAIL_SYMBOL} FAILED: {func}", _c.bold_red, no_color)
    print(header)
    if source:
        loc = _color_text(f"    File: {source}", _c.cyan, no_color)
        print(loc)
    if explain:
        print(explain)


def _print_warnings(caught_warnings, no_color):
    if not caught_warnings:
        return
    header = _color_text(f"\n{_WARN_SYMBOL} Warnings ({len(caught_warnings)}):", _c.yellow, no_color)
    print(header)
    for w in caught_warnings:
        loc = f"{w.filename}:{w.lineno}"
        msg = f"  {w.category.__name__}: {w.message}"
        print(_color_text(f"    {loc}", _c.cyan, no_color))
        print(_color_text(msg, _c.yellow, no_color))


def _print_summary(total, passed, failed, ignored, no_color, failures=None, verbose=False, elapsed=None):
    line = _SEPARATOR * 50
    print(_color_text(line, _c.intense_black, no_color))

    if verbose and failures:
        print(_color_text("\nFailures:", _c.bold_red, no_color))
        for result in failures:
            _print_failure_detail(result, no_color)
        print()

    parts = [f"Total: {total}", f"Passed: {passed}", f"Failed: {failed}"]
    if ignored:
        parts.append(f"Ignored: {ignored}")
    if elapsed is not None:
        parts.append(f"in {elapsed:.2f}s")
    summary = " | ".join(parts)

    if failed == 0:
        symbol = _PASS_SYMBOL
        summary = _color_text(f"{symbol} {summary}", _c.bold_green, no_color)
    else:
        symbol = _FAIL_SYMBOL
        summary = _color_text(f"{symbol} {summary}", _c.bold_red, no_color)
    print(summary)


def _classify(result, ignore_rules):
    if result["ok"]:
        return "pass", result["func_name"]
    if is_ignored(ignore_rules, result["exc_name"], result["source_file"]):
        return "ignored", f"{result['func_name']} -> {result['exc_name']}"
    return "fail", f"{result['func_name']} -> {result['exc_name']}"


def _print_setup(color):
    ver = '.'.join(map(str, sys.version_info[:3]))
    _s = f"platform: {sys.platform}, python {ver}, dummytest {__version__}"
    print(_color_text(_s, _c.cyan, color))

    import pathlib
    cwd = pathlib.Path.cwd()
    found = []
    if (cwd / "dummytest.ini").is_file():
        found.append("dummytest.ini")
    if (cwd / "pyproject.toml").is_file():
        found.append("pyproject.toml")
    if (cwd / ".dummytestignore").is_file():
        found.append(".dummytestignore")
    if found:
        cfg_line = f"config files: {', '.join(found)}"
        print(_color_text(cfg_line, _c.cyan, color))

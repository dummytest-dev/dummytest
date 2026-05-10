"""Loader/matcher for ``.dummytestignore``.

File format: one rule per line. Each rule is::

    <ExceptionName>[<file-glob>]

* ``<ExceptionName>`` matches against ``type(e).__name__`` of the test failure,
  or ``*`` to match any exception (including ``AssertionError``).
* The ``[...]`` part is optional; when omitted, the rule applies to any test
  file. The glob is fnmatch-style and tested against both the absolute path
  and the path relative to cwd, so users can write ``tests/legacy/*.py``.

Lines beginning with ``#`` and blank lines are ignored.

Examples::

    ImportError[tests/test_ignore.py]
    AssertionError[tests/legacy/*.py]
    *[tests/experimental/*.py]
    ImportError
"""

import fnmatch
import pathlib
import re


_RULE_RE = re.compile(r"^\s*(?P<exc>[A-Za-z_][A-Za-z0-9_]*|\*)\s*(?:\[(?P<glob>[^\]]*)\])?\s*$")


def load_ignore_rules(path):
    p = pathlib.Path(path)
    if not p.is_file():
        return []
    rules = []
    for raw in p.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = _RULE_RE.match(line)
        if not m:
            continue
        rules.append((m.group("exc"), m.group("glob")))
    return rules


def is_ignored(rules, exc_name, test_file):
    if not rules:
        return False
    abs_path = str(pathlib.Path(test_file).resolve()) if test_file else ""
    try:
        rel_path = str(pathlib.Path(test_file).resolve().relative_to(pathlib.Path.cwd()))
    except (ValueError, OSError):
        rel_path = abs_path
    rel_path = rel_path.replace("\\", "/")
    abs_path = abs_path.replace("\\", "/")

    for exc_pat, glob in rules:
        if exc_pat != "*" and exc_pat != exc_name:
            continue
        if glob is None:
            return True
        glob = glob.replace("\\", "/")
        if fnmatch.fnmatch(rel_path, glob) or fnmatch.fnmatch(abs_path, glob):
            return True
    return False

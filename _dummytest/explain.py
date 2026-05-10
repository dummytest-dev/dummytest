"""Dummytest-style assertion explanation."""

import ast
import linecache


_OPS = {
    ast.Eq: "==",
    ast.NotEq: "!=",
    ast.Lt: "<",
    ast.LtE: "<=",
    ast.Gt: ">",
    ast.GtE: ">=",
    ast.Is: "is",
    ast.IsNot: "is not",
    ast.In: "in",
    ast.NotIn: "not in",
}

_LINENO_WIDTH = 12


class _Unknown:
    def __repr__(self):
        return "<?>"


_UNKNOWN = _Unknown()


def _explain_assertion(exc_tb):
    tb = exc_tb
    while tb is not None and tb.tb_next is not None:
        tb = tb.tb_next
    if tb is None:
        return None

    frame = tb.tb_frame
    lineno = tb.tb_lineno
    filename = frame.f_code.co_filename
    src_line = linecache.getline(filename, lineno).rstrip("\n")
    stripped = src_line.strip()
    if not stripped.startswith("assert"):
        return None
    try:
        tree = ast.parse(stripped, mode="exec")
    except SyntaxError:
        return None
    if not tree.body or not isinstance(tree.body[0], ast.Assert):
        return None
    node = tree.body[0]

    def _eval(n):
        try:
            return eval(
                compile(ast.Expression(n), "<assert>", "eval"),
                frame.f_globals,
                frame.f_locals,
            )
        except Exception:
            return _UNKNOWN

    indent = src_line[:len(src_line) - len(src_line.lstrip())]
    test = node.test
    if isinstance(test, ast.Compare) and len(test.ops) == 1:
        op = _OPS.get(type(test.ops[0]))
        if op is None:
            evaluated = f"assert {_eval(test)!r}"
        else:
            lv = _eval(test.left)
            rv = _eval(test.comparators[0])
            evaluated = f"assert {lv!r} {op} {rv!r}"
    else:
        evaluated = f"assert {_eval(test)!r}"

    return (
        f"{lineno:>{_LINENO_WIDTH}} | {src_line}\n"
        f"{'':>{_LINENO_WIDTH}} | {indent}{evaluated}"
    )

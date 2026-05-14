# dummytest

Plugins, fixtures, workflows, unit and functional tests with Python.

## Install

```bash
pip install dummytest
```

## Usage

```bash
# Run tests in the tests/ directory
dummytest

# Run a specific test file
dummytest --test-file tests/test_assertions.py

# Run an inline assertion
dummytest "assert 1 + 1 == 2"

# Verbose mode (show tracebacks and failure details)
dummytest -v
```

## Fixtures

```python
import dummytest

@dummytest.fixture
def db():
    conn = connect()
    yield conn
    conn.close()

def test_query(db):
    assert db.execute("SELECT 1") is not None
```

Built-in fixtures: `tmp_path`, `capsys`, `monkeypatch`.

## Config

- `dummytest.ini` — INI config under `[dummytest]`
- `pyproject.toml` — TOML config under `[tool.dummytest]`
- `.dummytestignore` — ignore rules for expected failures

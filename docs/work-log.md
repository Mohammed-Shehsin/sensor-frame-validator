# Work Log

## Numeric grammar and regression check

- Defined numeric values as an optional ASCII sign, one or more ASCII digits, and an optional decimal point followed by one or more ASCII digits. Added matching and non-matching parameterized cases in both fields.
- Implemented a full-match check before float conversion. The test matrix now links the numeric-form categories to their tests.
- Before the deliberate mutation, `.\.venv\Scripts\python.exe -m pytest -q` completed with **72 passed**.
- Temporarily changed the temperature check from `-40 <= temperature_c` to `-40 < temperature_c`. Running `.\.venv\Scripts\python.exe -m pytest -q tests/test_parser.py::test_lower_boundaries_are_accepted` failed as expected: the frame `TEMP=-40;HUM=0` raised `SensorFrameError` at the lower-bound check (one failed test, exit code 1).
- Restored the inclusive `-40 <= temperature_c` check. The final `.\.venv\Scripts\python.exe -m pytest -q` completed with **72 passed**.

The lower-boundary regression test caught the defect because it explicitly expects the documented inclusive endpoint `-40` to produce a valid reading. Making the comparison exclusive violates that expectation and causes the test to fail.
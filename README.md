# Sensor Frame Validator

Sensor Frame Validator parses and validates a temperature and humidity reading from a text frame. For example, `TEMP=21.5;HUM=48` returns a structured reading with temperature `21.5` Celsius and humidity `48` percent.

## Windows Setup

Install Python 3.13, then create and activate a virtual environment from the project directory:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project with its test dependency and run the tests:

```powershell
python -m pip install ".[test]"
python -m pytest -q
```

If you prefer not to activate the environment, run these with `\.venv\Scripts\python.exe` instead of `python`.

## Frame Format and Validation

A frame has exactly two fields, in this order:

```text
TEMP=<number>;HUM=<number>
```

Whitespace is allowed around fields, keys, and values. Each number has this grammar after surrounding whitespace is removed:

```text
[+-]?[0-9]+(\.[0-9]+)?
```

The sign, digits, and decimal point are ASCII characters. Exponent notation, underscores, decimal commas, leading-dot decimals, and trailing-dot decimals are rejected. Temperature must be between -40 and 125 Celsius inclusive; humidity must be between 0 and 100 percent inclusive. Invalid frames raise `SensorFrameError`; valid frames return a `SensorReading`.

## Continuous Integration

The GitHub Actions workflow in `.github/workflows/tests.yml` is prepared to run on pushes, pull requests, and manual dispatch. It uses an Ubuntu runner, sets up Python 3.13, installs the package and pinned pytest test dependency with `python -m pip install ".[test]"`, then runs `python -m pytest -q`. This workflow has not been run on GitHub yet.

Passing tests provide evidence for the cases covered, but do not prove correctness for every possible input.
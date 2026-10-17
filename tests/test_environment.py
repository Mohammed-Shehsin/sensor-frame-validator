import sys


def test_python_313_or_newer_is_available():
    assert sys.version_info >= (3, 13)
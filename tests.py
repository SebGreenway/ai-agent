import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from functions.run_python import run_python_file


def test_run_python_main_py():
    result = run_python_file("calculator", "main.py")
    print("test_run_python_main_py result:")
    print(result)
    print()


def test_run_python_tests_py():
    result = run_python_file("calculator", "tests.py")
    print("test_run_python_tests_py result:")
    print(result)
    print()


def test_run_python_outside_dir():
    result = run_python_file("calculator", "../main.py")
    print("test_run_python_outside_dir result:")
    print(result)
    print()


def test_run_python_nonexistent():
    result = run_python_file("calculator", "nonexistent.py")
    print("test_run_python_nonexistent result:")
    print(result)
    print()


if __name__ == "__main__":
    test_run_python_main_py()
    test_run_python_tests_py()
    test_run_python_outside_dir()
    test_run_python_nonexistent()

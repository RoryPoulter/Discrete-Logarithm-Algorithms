"""The main script that will run the different algorithms and compare run-times.
"""


from time import time
from collections.abc import Callable
from discrete_log import baby_step_giant_step, pohlig_hellman, pollards_rho, utils


class Colours:
    """Terminal print colours. Code from:
    https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def fail(*args):
    """Dummy functin to fail all tests.

    Returns:
        int: 0 on all inputs.
    """
    _ = args
    return 0


def test_functions(functions: list[Callable], tests: list[tuple]) -> None:
    """Test suite for the multiple discrete logarithm algorithms.

    Args:
        functions (list[Callable]): A list of the functions to be tested.
        tests (list[tuple]): A list of tuples of values (g, h, p).
    """
    print("=============================Begin Test Suite=============================")
    passed_functions = []
    failed_functions = []
    for func in functions:
        print(f"  Testing function {func.__name__}")
        passed = 0
        total = len(tests)
        for test in tests:
            print(f"    g = {test[0]}, h = {test[1]}, p = {test[2]} | x = ", end='')
            start = time()
            x_result = func(*test)
            end = time()
            time_elapsed = end - start
            if x_result is not None and utils.verify(*test, x_result):
                print(f"{Colours.OKGREEN}{x_result} ✓ ({time_elapsed} s){Colours.ENDC}")
                passed += 1
            else:
                print(f"{Colours.FAIL}{x_result} X ({time_elapsed} s){Colours.ENDC}")
        if passed == total:
            passed_functions.append(func)
            print(f"{Colours.OKGREEN}  Passed [{passed}/{total}] tests: passed\n{Colours.ENDC}")
        else:
            failed_functions.append(func)
            print(f"{Colours.FAIL}  Passed [{passed}/{total}] tests: failed\n{Colours.ENDC}")

    if passed_functions:
        print(f"{Colours.OKGREEN}Functions passed: [{len(passed_functions)}/{len(functions)}]: {
            ", ".join([func.__name__ for func in passed_functions])}{Colours.ENDC}")
    if failed_functions:
        print(f"{Colours.FAIL}Functions failed: [{len(failed_functions)}/{len(functions)}]: {
            ", ".join([func.__name__ for func in failed_functions])}{Colours.ENDC}")
    print("==============================End Test Suite==============================")


def main():
    """Runs the DLP algorithms on random inputs and compares the run-times.
    """
    # [ ( g, h, p ) ]
    tests = [
        (2, 7, 11),
        (2, 435, 2579),
        (2, 5189, 94109),
        (2, 255439, 377327),
        (2, 5, 1019),
        (2, 2220359, 2674621),
        (2, 21854006, 78386653)
    ]
    functions = [
        baby_step_giant_step,
        pohlig_hellman,
        pollards_rho
    ]
    test_functions(functions, tests)


if __name__ == "__main__":
    main()

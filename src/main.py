"""The main script that will run the different algorithms and compare run-times.
"""


from time import time
from discrete_log import baby_step_giant_step, pohlig_hellman, pollards_rho, utils


def test_function(func, tests) -> None:
    """Test suite for discrete log functions.

    Args:
        func (function): The function to test.
    """
    print(f"Testing function {func.__name__}:")
    passed = 0
    total = len(tests)
    for test in tests:
        print(f"    g = {test[0]}, h = {test[1]}, p = {test[2]} | x = ", end='')
        start = time()
        x_result = func(*test)
        end = time()
        time_elapsed = end - start
        if x_result is not None and utils.verify(*test, x_result):
            print(f"{x_result} ✓ ({time_elapsed} s)")
            passed += 1
        else:
            print(f"{x_result} X ({time_elapsed} s)")
    print(f"Passed [{passed}/{total}] tests: {"passed" if passed == total else "failed"}\n")


def main():
    """Runs the DLP algorithms on random inputs and compares the run-times.
    """
    # [ ( g, h, p ) ]
    tests = [
        (2, 7, 11),
        (2, 435, 2579),
        (2, 5189, 94109),
        (2, 255439, 377327),
        (2, 5, 1019)
    ]
    test_function(baby_step_giant_step, tests)
    test_function(pohlig_hellman, tests)
    test_function(pollards_rho, tests)


if __name__ == "__main__":
    main()

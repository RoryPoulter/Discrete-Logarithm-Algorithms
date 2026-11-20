"""The main script that will run the different algorithms and compare run-times.
"""


from time import time
from random import randint
from collections.abc import Callable
from discrete_log import (baby_step_giant_step,
                          pohlig_hellman,
                          pollards_rho,
                          pollards_kangaroo,
                          parallel_pohlig_hellman,
                          utils)


# Terminal print colours. Code adapted from:
# https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
COLOURS = {
    "HEADER": '\033[95m',
    "OKBLUE": '\033[94m',
    "OKCYAN": '\033[96m',
    "OKGREEN": '\033[92m',
    "WARNING": '\033[93m',
    "FAIL": '\033[91m',
    "ENDC": '\033[0m',
    "BOLD": '\033[1m',
    "UNDERLINE": '\033[4m'
}


def fail(
    *args
    ) -> int:
    """Dummy functin to fail all tests.

    Returns:
        int: 0 on all inputs.
    """
    _ = args
    return 0


def fixed_test_functions(
    functions: list[Callable],
    tests: list[tuple]
    ) -> dict:
    """Test suite for the multiple discrete logarithm algorithms on fixed test cases.

    Args:
        functions (list[Callable]): A list of the functions to be tested.
        tests (list[tuple]): A list of tuples of values (g, h, p).

    Returns:
        dict: The results of the tests.
    """
    print("=============================Begin Test Suite=============================")

    print("Test cases:")
    for g, h, p in tests:
        smoothness = utils.smoothness(p-1)
        print(f"    {g=}, {h=}, {p=}, {smoothness=}")

    print("Begin tests:")
    passed_functions = []
    failed_functions = []
    results = {}
    for func in functions:
        print(f"  Testing function {func.__name__}")
        passed = 0
        total = len(tests)
        results[func.__name__] = []
        for test in tests:
            print(f"    g = {test[0]}, h = {test[1]}, p = {test[2]} | x = ", end='')
            start = time()
            x_result = func(*test)
            end = time()
            if x_result is not None and utils.verify(*test, x_result):
                print(f"{COLOURS["OKGREEN"]}{x_result} ✓ ({end - start} s){COLOURS["ENDC"]}")
                passed += 1
                results[func.__name__].append({"g": test[0],
                                               "h": test[1],
                                               "p": test[2],
                                               "x": x_result,
                                               "time": end - start})
            else:
                print(f"{COLOURS["FAIL"]}{x_result} X ({end - start} s){COLOURS["ENDC"]}")
        if passed == total:
            passed_functions.append(func)
            print(f"{COLOURS["OKGREEN"]}  Passed [{passed}/{total}] tests: passed\n{
                COLOURS["ENDC"]}")
        else:
            failed_functions.append(func)
            print(f"{COLOURS["FAIL"]}  Passed [{passed}/{total}] tests: failed\n{COLOURS["ENDC"]}")

    if passed_functions:
        print(f"{COLOURS["OKGREEN"]}Functions passed: [{len(passed_functions)}/{len(functions)}]: {
            ", ".join([func.__name__ for func in passed_functions])}{COLOURS["ENDC"]}")
    if failed_functions:
        print(f"{COLOURS["FAIL"]}Functions failed: [{len(failed_functions)}/{len(functions)}]: {
            ", ".join([func.__name__ for func in failed_functions])}{COLOURS["ENDC"]}")
    print("==============================End Test Suite==============================")
    return results


def random_test_functions(functions: list[Callable], g: int, p: int, num_tests: int = 10) -> dict:
    """Generates random tests from a generator and prime, and tests the funcitons.

    Args:
        functions (list[Callable]): The list of functions to test.
        g (int): The generator of the group.
        p (int): The prime base of the group.
        num_tests (int, optional): The number of random tests to generate. Defaults to 10.

    Returns:
        dict: The results of the tests.
    """

    tests = []
    for _ in range(num_tests):
        test = generate_random_test(g, p)
        tests.append(test)

    return fixed_test_functions(functions, tests)


def generate_random_test(g: int, p: int) -> tuple[int, int, int]:
    """Generates a random discrete log to automate testing on specific primes.

    Args:
        g (int): The generator of the group.
        p (int): The prime base of the group.

    Returns:
        tuple[int, int, int]: A tuple of (g, h, p)
    """
    x = randint(1, p-1)
    h = pow(g, x, p)
    return (g, h, p)


def main():
    """Runs the DLP algorithms on random inputs and compares the run-times.
    """
    # [ ( g, h, p ) ]
    basic_tests = [                     # Smoothness:
        (2, 7, 11),                     # 5
        (2, 435, 2579),                 # 1289
        (2, 5189, 94109),               # 3361
        (2, 255439, 377327),            # 5099
        (2, 5, 1019),                   # 509
        (2, 2220359, 2674621),          # 127
        (2, 21854006, 78386653),        # 75083
        (2, 956553292, 1001100283),     # 5573
    ]
    all_functions = [
        baby_step_giant_step,
        pollards_rho,
        pollards_kangaroo,
        pohlig_hellman,
        parallel_pohlig_hellman
    ]
    print("Testing all functions...")
    fixed_test_functions(all_functions, basic_tests)

    print("Testing serial vs parallel Pohlig-Hellman...")
    parallel_tests = [
        (2, 249617749644, 865849357141),    # 674117
        (2, 655562086919, 4580442851111),   # 9067
        (7894352216, 355407489, 604604729), # 997
        (2, 18625593847, 8696209053167)     # 5257683829
    ]
    fixed_test_functions([pohlig_hellman, parallel_pohlig_hellman], parallel_tests)

    print("Testing serial vs parallel Pohlig-Hellman on g=2, p=8696209053167...")
    results = random_test_functions([pohlig_hellman, parallel_pohlig_hellman], 2, 8696209053167)
    print(results)


if __name__ == "__main__":
    main()

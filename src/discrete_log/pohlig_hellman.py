"""Implementation of the Pohlig-Hellman algorithm.
"""


from math import prod
from .baby_step_giant_step import baby_step_giant_step
from .utils import mod_inverse


def prime_factorise(n: int) -> list[int]:
    """Finds the prime factorisation of an integer n such that:
        n = p_1^n_1 + p_2^n_2 + p_3^n_3 + ...

    Args:
        n (int): The composite number to be factorised.

    Returns:
        list[int]: The list of p_i^n_i which multiply to n
    """
    factors = []

    upper_bound = 1 + n // 2  # Upper bound for prime factors
    for p_i in range(2, upper_bound):
        count = 0
        while n % p_i == 0:
            n //= p_i
            count += 1
        if count > 0:
            factors.append(pow(p_i, count))
        if n == 1:
            break

    return factors


def calculate_x(p: int, prime_factors: list[int], subresults: list[int]) -> int:
    """Calculate the value of x using the Chinese Remainder Theorem

    Args:
        p (int): The prime base of the group
        prime_factors (list[int]): The prime factorisation of p-1
        subresults (list[int]): The solutions of x_i from each subgroup

    Returns:
        int: The value of x
    """
    n = p - 1
    # Find the partial products
    partial_products: list[int] = [n // p_i for p_i in prime_factors]
    modular_inverses: list[int] = list(map(mod_inverse, zip(partial_products, prime_factors)))

    x: int = sum(map(prod, zip(partial_products, subresults, modular_inverses)))
    return x % n


def pohlig_hellman(g: int, h: int, p: int, debug: bool = False) -> int:
    """Implementaiton of the Pohlig-Hellman algorithm for solving discrete logarithms.

    Args:
        g (int): The generator of the group
        h (int): The result of the modulo arithmetic
        p (int): The prime base of the group
        debug (bool, optional): If debug messages should be displayed. Defaults to False.

    Returns:
        int: The value of x
    """
    # 1. Find prime factorisation of p-1
    prime_factors: list[int] = prime_factorise(p-1)
    if debug:
        print(prime_factors)

    # 2. Solve each subproblem
    partial_products: list[int] = [(p-1) // p_i for p_i in prime_factors]  # Represents all r_i
    subresults: list[int] = []  # Represents all x_i
    for i in range(len(prime_factors)):
        g_i = pow(g, partial_products[i], p)
        h_i = pow(h, partial_products[i], p)
        if debug:
            try: 
                print(f"{i=}: {g_i=}, {h_i=}")
            except ValueError:
                print(f"{i=}: too long...")
        x_i = baby_step_giant_step(g_i, h_i, p)
        if debug:
            print(f"{x_i=}")
        subresults.append(x_i)

    # 3. Calculate x
    x = calculate_x(p, prime_factors, subresults)
    return x


if __name__ == "__main__":
    print(pohlig_hellman(2, 7, 11))
    print(calculate_x(p=11,
                      prime_factors=[2,5],
                      subresults=[1,2]))

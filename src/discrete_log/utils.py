"""Utility functions for the Discrete Logarithm algorithms.
"""


from math import gcd, isqrt, prod
from .baby_step_giant_step import baby_step_giant_step


def verify(
    g: int,
    h: int,
    p: int,
    x: int
    ) -> bool:
    """Verifier function for the results of the discrete log algorithms.

    Args:
        g (int): The generator of the group.
        h (int): The value of `g ^ x mod p`
        p (int): The prime base of the group.
        x (int): The exponent of `g` to obtain `h`.

    Returns:
        bool: If the result is correct.
    """
    return h == pow(g, x, p)


def mod_inverse(
    args: tuple[int]
    ) -> int:
    """Finds the modular multiplicative inverse of a number n under m. Code adapted from:
    https://www.geeksforgeeks.org/dsa/multiplicative-inverse-under-modulo-m/

    Args:
        args (tuple[int]): The original-modulo pair (n, m).

    Returns:
        int: The inverse of n.
    """
    n = args[0]
    m = args[1]
    # Check if inverse exists
    if gcd(n, m) != 1:
        return -1

    m0 = m
    y = 0
    x = 1

    if m == 1:
        return 0

    while n > 1:
        # q is quotient
        q = n // m
        t = m

        # m is remainder now, process same as Euclid's algo
        m = n % m
        n = t
        t = y

        # Update y and x
        y = x - q * y
        x = t

    # Make x positive
    if x < 0:
        x = x + m0

    return x


def chinese_remainder(
    p: int,
    prime_factors: list[int],
    subresults: list[int]
    ) -> int:
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


def prime_factorise(
    n: int
    ) -> list[int]:
    """Finds the prime factorisation of an integer n such that:
        n = p_1^n_1 + p_2^n_2 + p_3^n_3 + ...

    Args:
        n (int): The composite number to be factorised.

    Returns:
        list[int]: The list of p_i^n_i which multiply to n
    """
    if n < 2:
        return []

    factors = []
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    if count > 0:
        factors.append(pow(2, count))

    factor = 3
    while factor <= isqrt(n):
        count = 0
        while n % factor == 0:
            n //= factor
            count += 1
        if count > 0:
            factors.append(pow(factor, count))
        factor += 2

    if n > 1:
        factors.append(n)

    return factors


def smoothness(
    n: int
    ) -> int:
    """Calculates the smoothness of an integer - the largest prime factor.

    Args:
        n (int): The integer.

    Returns:
        int: The smoothness of `n`.
    """
    if n < 2:
        return 2

    max_p = 1
    if n % 2 == 0:
        max_p = 2
        while n % 2 == 0:
            n //= 2

    factor = 3
    while factor <= isqrt(n):
        if n % factor == 0:
            max_p = factor
            while n % factor == 0:
                n //= factor
        factor += 2

    if n > 1:
        max_p = n

    return max_p


def solve_ph_subgroup(
    g: int,
    h: int,
    p: int,
    n_i: int
    ) -> int | None:
    """Solver for the subgroup of G for Pohlig-Hellman.

    Args:
        g (int): The generator of the group G.
        h (int): The result of the modulo arithmetic.
        p (int): The prime base of the group.
        n_i (int): The power, equal to N / p_i.

    Returns:
        int | None: The discrete logarithm of the subgroup.
    """
    g_i = pow(g, n_i, p)
    h_i = pow(h, n_i, p)
    x_i = baby_step_giant_step(g_i, h_i, p, n_i)
    if x_i is not None:
        return x_i
    # If using n_i for the group order fails, use p-1.
    return baby_step_giant_step(g_i, h_i, p)


def is_prime(
    n: int
    ) -> bool:
    """Checks if an integer is a prime.

    Args:
        n (int): An integer.

    Returns:
        bool: Boolean value for if the integer is a prime.
    """
    return n == smoothness(n)


def is_safe_prime(
    n: int
    ) -> bool:
    """Checks if an integer is a safe prime: n = 2p + 1 where p is also prime.

    Args:
        n (int): An integer.

    Returns:
        bool: Boolean value for it the integer is a safe prime.
    """
    return is_prime(n) and 2 * smoothness(n-1) + 1 == n


if __name__ == "__main__":
    # print(smoothness(1001100283))
    print(smoothness(1001100283-1))
    print(pow(2, 6342175, 1001100283))
    print(verify(2, 956553292, 1001100283, 6342175))

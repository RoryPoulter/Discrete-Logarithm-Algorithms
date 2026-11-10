"""Utility functions for the Discrete Logarithm algorithms.
`mod_inverse` function adapted from: 
https://www.geeksforgeeks.org/dsa/multiplicative-inverse-under-modulo-m/
"""


from math import gcd


def verify(g: int, h: int, p: int, x: int) -> bool:
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


def mod_inverse(args: tuple[int]) -> int:
    """Finds the modular multiplicative inverse of a number n under m.

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

"""Implementation of the Pollard's Rho algorithm.
"""


from math import gcd
from random import randrange
from .utils import verify


def pollard_rho_step(pollard_tuple: list[int], base: tuple[int]) -> list[int]:
    """Computes one step on the tuple [x_i, a_i, b_i].

    Args:
        round (list[int]): The tuple [x_i, a_i, b_i].
        base (tuple[int]): The tuple (g, h, p, n).
    Returns:
        list[int]: The next tuple [x_i+1, a_i+1, b_i+1].
    """
    g, h, p, n = base
    x, a, b = pollard_tuple
    r = x % 3
    n = p-1
    if r == 0:
        return [(x*x) % p, (2*a) % n, (2*b) % n]
    if r == 1:
        return [(x*g) % p, (a+1) % n, b]
    return [(x*h) % p, a, (b+1) % n]


def pollards_rho(g: int, h: int, p: int, max_restarts: int = 20) -> int | None:
    """Calculates the discrete logarithm using Pollard's Rho algorithm.

    Args:
        g (int): The generator.
        h (int): The modular result.
        p (int): The prime base.
        max_restarts (int, optional): The max number of restarts for the algorithm. Defaults to 20.

    Returns:
        int | None: The discrete logarithm, or `None` if not found.
    """
    base = (g, h, p, p-1)  # Tuple for base knowledge, need not change.
    for attempt in range(max_restarts+1):
        # First attempt starts at [1, 0, 0] for slow and fast tuples.
        if attempt == 0:
            a0 = 0
            b0 = 0
        # Subsequent attempts use random exponents.
        else:
            a0 = randrange(p-1)
            b0 = randrange(p-1)
        # Calculate start avlue based on the exponents a0, b0
        start = (pow(g, a0, p) * pow(h, b0, p)) % p

        # Initialise the slow and fast tuples;
        # fast tuple takes 2 steps per step taken by slow tuple.
        slow_tuple = [start, a0, b0]
        fast_tuple = [start, a0, b0]

        for _ in range(p-1):
            slow_tuple = pollard_rho_step(slow_tuple, base)
            fast_tuple = pollard_rho_step(pollard_rho_step(fast_tuple, base), base)
            if slow_tuple[0] == fast_tuple[0]:
                break
        else:
            continue  # No collision found, restart.

        r = (fast_tuple[2] - slow_tuple[2]) % (p-1)
        s = (slow_tuple[1] - fast_tuple[1]) % (p-1)
        if r == 0:
            continue  # Collision is useless, restart.

        d = gcd(r, p-1)
        if s % d != 0:
            continue

        x = calculate_x(base, r, s, d)
        if x is not None:
            return x

    # If all attempts have failed, return `None`.
    return None


def calculate_x(base: tuple[int], r: int, s: int, d: int) -> int | None:
    """Calculate x from r, s, and d.

    Args:
        base (tuple[int]): The tuple (g, h, p, n).
        r (int): The difference of b_2i and b_i.
        s (int): The difference of a_i and a_21.
        d (int): The GCD of r and n.

    Returns:
        int | None: The discrete log x, or `None` if not found.
    """
    g, h, p, n = base
    r //= d
    s //= d
    m = n // d

    x0 = (s * pow(r, -1, m)) % m if m > 1 else 0

    for k in range(d):
        x = x0 + k * m
        if verify(g, h, p, x):
            return x
    return None


if __name__ == "__main__":
    print(pollards_rho(2, 7, 11))  # 7

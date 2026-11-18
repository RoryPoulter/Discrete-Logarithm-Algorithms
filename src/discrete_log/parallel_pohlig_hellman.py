"""Parallel implementation of the Pohlig-Hellman algorithm to calculate discrete logarithms.
"""


from concurrent.futures import ProcessPoolExecutor
from .utils import chinese_remainder, prime_factorise, solve_ph_subgroup
from .pohlig_hellman import pohlig_hellman


def parallel_pohlig_hellman(
    g: int,
    h: int,
    p: int,
    max_threads: int = 4
    ) -> int:
    """Pohlig-Hellman algorithm for calculating discrete logarithms, using threading. If
    `max_threads = 1`, then act as serial Pohlig-Hellman.

    Args:
        g (int): The generator of the group.
        h (int): The result of the modulo arithmetic.
        p (int): The prime base of the group.
        max_threads (int, optional): The maximum number of threads allowed. Defaults to 4.

    Raises:
        ValueError: Raised if `max_threads < 1`.

    Returns:
        int: The discrete logarithm `x`.
    """
    if max_threads < 1:
        raise ValueError("max_threads must be at least 1")

    if max_threads == 1:
        return pohlig_hellman(g, h, p)

    # 1. Find the prime factorisation of the order of the group N.
    prime_factors: list[int] = prime_factorise(p-1)

    # 2. Solve each subproblem.
    partial_products: list[int] = [(p-1) // p_i for p_i in prime_factors]  # Represents all r_i
    subresults: list[int] = []

    workers = max(1, min(max_threads, len(prime_factors)))
    with ProcessPoolExecutor(max_workers=workers) as executor:
        subresults = list(executor.map(
            solve_ph_subgroup,
            [g] * len(partial_products),
            [h] * len(partial_products),
            [p] * len(partial_products),
            partial_products
        ))

    # 3. Calculate x using the Chinese Remainder Theorem.
    x = chinese_remainder(p, prime_factors, subresults)
    return x


if __name__ == "__main__":
    assert parallel_pohlig_hellman(2, 7, 11) == 7

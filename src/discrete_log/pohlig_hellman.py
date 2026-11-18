"""Implementation of the Pohlig-Hellman algorithm.
"""


from .utils import chinese_remainder, prime_factorise, solve_ph_subgroup


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
    # Represent all n_i
    partial_products: list[int] = [(p-1) // p_i for p_i in prime_factors]
    # Represent all x_i
    subresults: list[int] = [solve_ph_subgroup(g, h, p, n_i) for n_i in partial_products]

    # 3. Calculate x
    x = chinese_remainder(p, prime_factors, subresults)
    return x


if __name__ == "__main__":
    print(pohlig_hellman(2, 7, 11))

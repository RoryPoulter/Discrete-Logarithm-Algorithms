"""Implementation of the Pohlig-Hellman algorithm.
"""


from .baby_step_giant_step import baby_step_giant_step
from .utils import chinese_remainder, prime_factorise


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
    x = chinese_remainder(p, prime_factors, subresults)
    return x


if __name__ == "__main__":
    print(pohlig_hellman(2, 7, 11))

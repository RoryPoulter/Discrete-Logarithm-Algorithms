"""Implementation of the Baby-Step Giant-Step algorithm, adapted from:
https://gist.github.com/0xTowel/b4e7233fc86d8bb49698e4f1318a5a73
"""


from math import ceil, sqrt


def baby_step_giant_step(g: int, h: int, p: int) -> int | None:
    """Solve for x in h = g^x mod p given a prime p.
    If p is not prime, you shouldn't use BSGS anyway.

    Args:
        g (int): The generator of the group G
        h (int): The result of g^x mod p
        p (int): The prime base of the group G

    Returns:
        int | None: The value for x such that h = g^x mod p
    """
    n = ceil(sqrt(p - 1))  # phi(p) is p-1 if p is prime

    # Store hashmap of g^{1...m} (mod p). Baby step.
    tbl = {pow(g, i, p): i for i in range(n)}

    # Precompute via Fermat's Little Theorem
    c = pow(g, n * (p - 2), p)

    # Search for an equivalence in the table. Giant step.
    for j in range(n):
        y = (h * pow(c, j, p)) % p
        if y in tbl:
            return j * n + tbl[y]

    # Solution not found
    return None


# Example code
if __name__ == "__main__":
    print(baby_step_giant_step(2, 7, 11))  # 7
    print(baby_step_giant_step(7894352216, 355407489, 604604729))  # 102900819

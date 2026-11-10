"""Implementation of the Pollard's Kangaroo algorithm.
"""


def pollards_kangaroo(g: int, h: int, p: int) -> int:
    """Implementaiton of the Pollard's Kangaroo algorithm for solving discrete logarithms.

    Args:
        g (int): The generator.
        h (int): The modular result.
        p (int): The prime base.

    Returns:
        int: The discrete logarithm x.
    """
    print(g, h, p)


if __name__ == "__main__":
    assert pollards_kangaroo(2, 7, 11) == 7

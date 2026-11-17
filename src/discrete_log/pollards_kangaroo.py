"""Implementation of the Pollard's Kangaroo algorithm.
"""


from math import ceil, log2, sqrt
from .baby_step_giant_step import baby_step_giant_step
from .utils import verify


def pollards_kangaroo_step(
    value: int,
    offset: int,
    steps: tuple,
    step_count: int,
    base: tuple[int, int]
    ) -> tuple[int, int]:
    """Performs a single step of the Pollard's Kangaroo alorithm for calculating discrete
    logarithms.

    Args:
        value (int): The current group value.
        offset (int): The partition offset.
        steps (tuple): The available jump distances.
        step_count (int): The number of jump distances.
        base (tuple[int, int]): The tuple (g, p).

    Returns:
        tuple[int, int]: The new value, and the jump.
    """
    g, p = base
    mixed = (value ^ (value >> 16)) * (0x45D9F3B + 2 * offset)
    mixed = (mixed ^ (mixed >> 16)) & 0xFFFFFFFF
    distance = steps[mixed % step_count]
    return (value * pow(g, distance, p)) % p, distance


def pollards_kangaroo(
    g: int,
    h: int,
    p: int
    ) -> int | None:
    """Solve `h = g**x (mod p)` using Pollard's Kangaroo algorithm.

    Args:
        g (int): The generator.
        h (int): The modular result.
        p (int): The prime base.

    Returns:
        int | None: The discrete logarithm x, or ``None`` if no collision is
            found.
    """
    if (p-1) <= 0:
        return None

    # The exponent is known to lie in [0, p - 2].  A tame walk starting at
    # g**(p - 1) is therefore equivalent to starting at the upper endpoint.
    average_step = ceil(sqrt(p-1))
    step_count = max(1, ceil(log2(average_step)) + 1)
    steps = tuple(1 << index for index in range(step_count))

    tame_limit = 8 * average_step
    wild_limit = (p-1) + tame_limit

    # A single deterministic partition can place the walks in disjoint
    # cycles, so retry with shifted partitions when no collision is found.
    for offset in range(max(64, step_count)):
        tame_path: dict[int, int] = {}
        value = 1
        distance = 0
        while distance <= tame_limit:
            tame_path.setdefault(value, distance)
            value, jump = pollards_kangaroo_step(value, offset, steps, step_count, (g, p))
            distance += jump

        value = h % p
        distance = 0
        while distance <= wild_limit:
            tame_distance = tame_path.get(value)
            if tame_distance is not None:
                candidate = (tame_distance - distance) % (p-1)
                if verify(g, h, p, candidate):
                    return candidate

            value, jump = pollards_kangaroo_step(value, offset, steps, step_count, (g, p))
            distance += jump

    # The walk is probabilistic; use the exact solver if all bounded walks
    # miss a collision, rather than reporting a false failure.
    return baby_step_giant_step(g, h, p)


if __name__ == "__main__":
    assert pollards_kangaroo(2, 7, 11) == 7

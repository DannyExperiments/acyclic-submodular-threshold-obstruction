"""Check the adaptation of Simmons–Bansal–Cheriyan, Example 2."""
from collections import Counter
from itertools import combinations, product

EXAMPLE = (
    (1, 3, 5, 7), (2, 3, 6, 7), (4, 5, 6, 7),
    (2, 6), (4, 5), (4, 6), (3, 7), (5, 7), (6, 7),
    (3,), (4,), (5,), (6,), (7,), (4, 5, 7),
)
# Value at each mask on active ground set {1,...,7}; assign weight 1 << (i-1) to i.
F_VALUES = (
    -8, 1, 1, 4, -1, 2, 2, 5, -1, 4, 4, 3, 6, 5, 5, 4,
    -3, 2, 6, 5, 2, 1, 5, 4, 0, 5, 5, 4, 5, 4, 4, 3,
    -3, 4, 0, 3, 2, 5, 1, 4, 0, 3, 3, 2, 5, 4, 4, 3,
    2, 5, 5, 4, 5, 4, 4, 3, 1, 4, 4, 3, 4, 3, 3, 2,
    -6, 2, 2, 5, -2, 1, 1, 4, 1, 5, 5, 4, 5, 4, 4, 3,
    -3, 1, 5, 4, 1, 0, 4, 3, 0, 4, 4, 3, 4, 3, 3, 2,
    -2, 5, 1, 4, 1, 4, 0, 3, 1, 4, 4, 3, 4, 3, 3, 2,
    1, 4, 4, 3, 4, 3, 3, 2, 0, 3, 3, 2, 3, 2, 2, 1,
)


def check_related_example(check_family, dependency, topological_sizes):
    # Original 8-point example and its 7-point active-ground version.
    for n, shift, exact_counts in ((7, 1, (3494, 14)), (8, 0, (8402, 16))):
        def mask(items):
            return sum(1 << (i-shift) for i in items)

        universe = frozenset(range(1 << n))
        full = max(universe)
        family = frozenset(map(mask, EXAMPLE))
        a, b = mask((3,)), mask((4,))
        assert {a, b} <= family and not ({a | b, a & b} & family)
        with_bottom = family | {0}
        check_family(universe, with_bottom)
        topological_sizes(universe, dependency(universe, with_bottom))

        symmetric = family | {full ^ a for a in family} | {0, full}
        assert len(symmetric) == 32
        check_family(universe, symmetric)
        arcs = dependency(universe, symmetric)
        assert (len(arcs), len(topological_sizes(universe, arcs))) == exact_counts

        v1, v2, v3 = map(mask, EXAMPLE[:3])
        d12, d21 = v1 & ~v2, v2 & ~v1
        u3 = v3 & ~d12
        combined = Counter()
        for a, b in ((v1, v2), (d12, v3), (d21, u3)):
            combined.update((a, b))
            combined.subtract((a & ~b, b & ~a))
        assert +combined == {v1: 1, v2: 1, v3: 1}
        assert -combined == {mask((1,)): 1, mask((2,)): 1, mask((4, 7)): 1}
        assert set(+combined) <= symmetric and not (set(-combined) & symmetric)

        if n == 7:
            values = F_VALUES
        else:
            # Element 0 is unused in the original family. Add modular cost 9 for it.
            values = tuple(F_VALUES[a >> 1] + 9*(a & 1) for a in range(1 << n))
        assert {a for a in universe if values[a] < 1} == with_bottom
        assert all(values[a] + values[b] >= values[a | b] + values[a & b]
                   for a, b in product(universe, repeat=2))
        print(f"Prior example on {n} ground elements: adding the empty set admits an exact threshold; "
              f"symmetric adaptation has 32 members, {exact_counts[0]:,} arcs and {exact_counts[1]} layers.")

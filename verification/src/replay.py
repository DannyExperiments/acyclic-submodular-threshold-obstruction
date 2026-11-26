#!/usr/bin/env python3
"""Check the explicit finite lattice witness and the closest literature adaptation."""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
from runpy import run_path

P = frozenset((1, 5, 7, 9, 25, 44, 45, 47, 61))
LAYERS = (
    (18, 22, 26, 30, 50, 54, 58),
    (10, 14, 19, 20, 28, 34, 38, 42, 48, 51, 52, 56, 62),
    (2, 6, 16, 24, 32, 35, 49, 55, 59),
    (23, 27, 33, 36, 40, 43, 46, 53, 60),
    (11, 21, 31, 39, 57),
    (3, 12, 17, 37, 41),
    (4, 8),
    (0, 15, 29),
    (13, 63),
    (7, 25, 44),
    (47, 61),
    (5, 9),
    (1,),
    (45,),
)
CORNERS = (
    (1, 44, 45), (5, 9, 1), (5, 25, 1), (5, 44, 45), (7, 9, 1),
    (7, 25, 1), (7, 44, 47), (7, 45, 47), (7, 61, 5), (9, 44, 45),
    (25, 44, 61), (25, 45, 61), (25, 47, 9), (47, 61, 45),
)
ROWS = ((7, 25, 31, 1), (31, 44, 63, 12), (12, 1, 13, 0))
REDUCED = frozenset((0, 1, 4, 5, 7, 8, 9, 12, 13, 15, 25, 29, 31, 44, 45, 47, 61, 63))


def check_family(universe, family):
    assert family <= universe
    assert all((a | b) in family or (a & b) in family for a, b in product(family, repeat=2))
    assert all((a | b) in universe and (a & b) in universe for a, b in product(universe, repeat=2))


def dependency(universe, family):
    arcs = set(product(universe - family, family))
    for a, c in product(universe, family):
        for b, other in ((a | c, a & c), (a & c, a | c)):
            if (a in family) == (b in family) and other not in family:
                arcs.add((a, b))
    return arcs


def topological_sizes(universe, arcs):
    todo = set(universe)
    sizes = []
    while todo:
        sources = todo - {b for a, b in arcs if a in todo}
        assert sources, "Dependency digraph has a cycle"
        sizes.append(len(sources))
        todo -= sources
    return sizes


def expand_elementary(a, b, n=6):
    """Decompose one meet/join row into elementary square rows on B_n."""
    base = a & b
    left = [1 << i for i in range(n) if (a & ~b) & (1 << i)]
    right = [1 << i for i in range(n) if (b & ~a) & (1 << i)]
    for i in left:
        smaller = base
        for j in right:
            yield smaller, i, j
            smaller |= j
        base |= i


def row_vector(a, b):
    terms = Counter((a, b))
    terms.subtract((a | b, a & b))
    return terms


def check_witness():
    lattice = frozenset(range(64))
    check_family(lattice, P)
    pairs = {(a, b) for a, b in combinations(sorted(P), 2) if (a | b) not in (a, b)}
    assert pairs == {(a, b) for a, b, _ in CORNERS}
    assert all(c in P and c in (a | b, a & b) for a, b, c in CORNERS)
    arcs = dependency(lattice, P)
    ranks = {a: i for i, layer in enumerate(LAYERS) for a in layer}
    assert sum(map(len, LAYERS)) == len(lattice) == len(ranks)
    assert set(ranks) == lattice and all(ranks[a] < ranks[b] for a, b in arcs)
    assert topological_sizes(lattice, arcs) == list(map(len, LAYERS))
    assert len(arcs) == 789 and len(arcs - set(product(lattice - P, P))) == 294
    print("B6: 14 incomparable pairs, 789 dependency arcs, 14 layers.")

    generated = set(P)
    while True:
        expanded = {c for a, b in product(generated, repeat=2) for c in (a | b, a & b)}
        if expanded == generated:
            break
        generated = expanded
    assert generated == REDUCED and len(generated) == 18
    check_family(REDUCED, P)
    reduced_arcs = dependency(REDUCED, P)
    assert reduced_arcs == {(a, b) for a, b in arcs if a in REDUCED and b in REDUCED}
    assert len(reduced_arcs) == 120
    print("Generated sublattice: 18 elements, 120 dependency arcs, induced subgraph.")

    combined = Counter()
    elementary_count = 0
    for a, b, union, meet in ROWS:
        assert {a, b, union, meet} <= REDUCED
        assert (union, meet) == (a | b, a & b)
        vector = row_vector(a, b)
        combined.update(vector)
        elementary = Counter()
        for base, i, j in expand_elementary(a, b):
            elementary.update(row_vector(base | i, base | j))
            elementary_count += 1
        assert +vector == +elementary and -vector == -elementary
    assert +combined == {7: 1, 25: 1, 44: 1}
    assert -combined == {0: 1, 13: 1, 63: 1}
    assert set(+combined) <= P and not (set(-combined) & P)
    assert all(sum(coef for a, coef in combined.items() if a & (1 << bit)) == 0 for bit in range(6))
    print(f"Three meet/join rows, {elementary_count} elementary squares, exact sign certificate.")


if __name__ == "__main__":
    check_witness()
    companion = Path(__file__).with_name("related_example.py")
    related = run_path(str(companion))
    related["check_related_example"](check_family, dependency, topological_sizes)
    print("PASS: both ambient witnesses and the literature comparison.")

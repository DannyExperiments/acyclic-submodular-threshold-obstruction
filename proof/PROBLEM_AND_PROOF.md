# Q335: acyclic but not order-induced

**Theorem.** Elbracht's Question 5.1.6 has a positive answer, even when the ambient lattice is the entire Boolean lattice on six elements. The same family works in its generated 18-element sublattice.

Use the Boolean lattice on six elements, identifying each subset with its binary integer mask. Thus join is bitwise OR and meet is bitwise AND. Let
P = {1, 5, 7, 9, 25, 44, 45, 47, 61}.

## Structural closure

A comparable pair has both its join and meet in P. The complete list for distinct incomparable pairs follows, with a witness in P from either corner:

| a | b | corner in P |
|--:|--:|--:|
|1|44|45|
|5|9|1|
|5|25|1|
|5|44|45|
|7|9|1|
|7|25|1|
|7|44|47|
|7|45|47|
|7|61|5|
|9|44|45|
|25|44|61|
|25|45|61|
|25|47|9|
|47|61|45|

## Acyclic dependency graph

Here is an explicit topological layering for the entire 64-element Boolean lattice:

~~~
[18,22,26,30,50,54,58]
[10,14,19,20,28,34,38,42,48,51,52,56,62]
[2,6,16,24,32,35,49,55,59]
[23,27,33,36,40,43,46,53,60]
[11,21,31,39,57]
[3,12,17,37,41]
[4,8]
[0,15,29]
[13,63]
[7,25,44]
[47,61]
[5,9]
[1]
[45]
~~~

Define h(a) as the row of a in this table. All outside vertices precede all inside vertices. For remaining arcs, the full check is: for each a ∈ {0,…,63}, and each c in the displayed P, form (b,d)=(a OR c,a AND c) and (a AND c,a OR c); if d is outside P and a,b have the same membership, then h(a)<h(b). This gives 294 distinct same-membership arcs, plus 495 outside-to-inside arcs. These finite claims are exactly replayable; no numerical procedure or search claim is needed for acyclicity.

## No submodular threshold

Assume P = {u : f(u)<k} for a submodular f. Apply submodularity to these three pairs, whose corners are shown:

| input | join | meet |
|:--|--:|--:|
|(7,25)|31|1|
|(31,44)|63|12|
|(12,1)|13|0|

Summing, the terms for 1, 12 and 31 cancel, giving
f(63)+f(13)+f(0) ≤ f(7)+f(25)+f(44).
Every left term is at least k; every right term is strictly less than k. This is a contradiction, without needing f or k to be nonnegative.

The generated sublattice is {0,1,4,5,7,8,9,12,13,15,25,29,31,44,45,47,61,63}. It contains every vertex in the three-inequality certificate, and its dependency graph is the induced subgraph on these vertices, since all auxiliary witnesses c are in P and its lattice operations agree. This gives the smaller witness.

## Scope and sources

- [Elbracht dissertation, Question 5.1.6](https://www.math.uni-hamburg.de/spag/dm/papers/Dissertation_Christian_Elbracht.pdf).
- [Elbracht, Kneip and Teegen, Question 4.5](https://arxiv.org/html/2103.13162v2#S4) is the equivalent article statement. Its earlier counterexample to order inducibility has a cyclic dependency graph; the present point is acyclicity.
- [Pinned catalog Q335](https://github.com/10m-u/open-problems-catalog/blob/ca8d4d44ba3db527f19f28928c240168f545ecfe/problems/mathematics/combinatorics-graph-theory-part-1.md#q335).

The [literature audit](../audits/public_safe_reports/LITERATURE_AUDIT.md) details the adaptation of the earlier Simmons–Bansal–Cheriyan family and the exact scope of that overlap. The paper includes the finite duality appendix.

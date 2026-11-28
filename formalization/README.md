# Lean certificate

`Q335.witness` is checked using Lean 4.30.0 and its standard library.

On the 64 six-bit masks, the specified nine-member family satisfies the corner condition and its dependency relation has no directed cycle. The three submodularity inequalities contradict a strict-threshold representation in the ordered algebraic interface used in the file. The correspondence with the powerset model, specialization to real values, and the eighteen-element sublattice are explained in the paper.

[Source](Q335Corners.lean) · [Verification workflow](../.github/workflows/lean.yml)

To replay from the repository root with Lean 4.30.0 installed, run

```sh
lean -DwarningAsError=true formalization/Q335Corners.lean
```

The source requests an axiom report. The GitHub Actions workflow downloads the pinned compiler, verifies its SHA-256 and checks the source with warnings treated as errors.

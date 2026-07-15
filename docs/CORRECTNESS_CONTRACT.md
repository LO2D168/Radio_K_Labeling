# Correctness Contract

This document defines the behavior that a refactor must preserve. A result is
not considered equivalent merely because a solver terminates successfully.

## Problem definition

For a graph `G`, the repository sets `k` to the graph diameter. A labeling
`c: V(G) -> Z` is feasible when, for every pair of vertices `u` and `v`,

```text
|c(u) - c(v)| >= k - dist(u, v) + 1.
```

The objective reported by the legacy experiments is the largest 1-based label
minus one. This offset must remain explicit at the output boundary.

## Representation contracts

- Vertices in adjacency lists and distance matrices are numbered `1..n`; index
  zero is unused.
- `k` is computed from finite entries of the distance matrix, not the filename.
- SAT order variables occupy `1..n*span`. A positive literal is decoded by the
  original `(vertex, label)` mapping before validation.
- Incremental methods reuse one solver object and retain added clauses.
- Assumption methods keep the base CNF unchanged and pass temporary assumptions.
- Symmetry-breaking clauses are present only in symmetric variants.
- Binary MIP variants and the CP variant are distinct models: the former add an
  all-different constraint, while the latter does not.

## Validation requirements

Every accepted labeling must pass the distance inequality independently of the
solver model. Tests cover BFS distances, the bound formula, Matrix Market
input, SAT decoding, and both valid and invalid labelings.

The `dataset/` files currently present in this checkout are empty placeholders.
End-to-end solver verification therefore requires the original Matrix Market
data to be restored before publication.

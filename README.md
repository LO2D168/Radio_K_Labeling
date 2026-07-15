# Radio K-Labeling

Research code for computing radio `k`-labelings of graphs with SAT and
mathematical-programming models.

## Problem

For a graph `G`, this project sets `k = diam(G)` and searches for an integer
labeling `c` satisfying

```text
|c(u) - c(v)| >= k - dist(u, v) + 1
```

for every pair of vertices. The reported objective is the largest 1-based
label minus one, matching the original experiment scripts.

## Repository status

The repository is being converted from a collection of copied experiment
scripts into a package with shared validation and reproducibility tooling. The
new core is under `src/radio_k_labeling/`. The historical SAT and CPLEX/Gurobi
directories are retained while their variants are audited individually.

The checked-in `dataset/*.mtx` files are currently zero-byte placeholders. The
original Matrix Market data must be restored before running the full experiments
or reproducing paper tables. The test suite uses small temporary graph fixtures
and does not modify `dataset/`.

## Installation

```bash
python -m pip install -e ".[dev]"
```

CPLEX and Gurobi are optional and require separate installations and valid
licenses. See `docs/REPRODUCIBILITY.md` before collecting benchmark results.

## Basic use

The package currently provides a safe Matrix Market inspection command:

```bash
radio-k-label path/to/graph.mtx
```

Shared Python APIs are available for BFS distances, bounds, SAT variable
decoding, Matrix Market input, and independent labeling validation. The legacy
solver drivers are not yet advertised as a stable unified CLI because several
directories contain incomplete or historically inconsistent variants.

## Methods

The legacy tree contains rebuild-based SAT, incremental SAT, direct one-hot
encodings, symmetry-breaking variants, assumption-based variants, CPLEX CP,
CPLEX binary MIP, and Gurobi models. These models differ in more than solver
name. In particular, the binary MIP models include an all-different constraint
that the CP model does not. See `docs/METHODS.md`.

All working SAT implementations currently use PySAT's `Cadical195` binding.
Directory names containing `CMS` or `Glucose` are not evidence of those solver
backends and require separate verification before being cited as experiments.

## Correctness and reproducibility

`docs/CORRECTNESS_CONTRACT.md` records the representation and objective
contracts that a refactor must preserve. `docs/REPRODUCIBILITY.md` lists the
environment, data, and result metadata required for a paper submission.

Run the tests with:

```bash
python -m pytest
```

## License and citation

The code is released under the MIT License. Citation metadata is in
`CITATION.cff`; replace its repository and paper fields with the final project
values before publication.

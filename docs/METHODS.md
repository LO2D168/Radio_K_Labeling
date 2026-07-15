# Methods

The original tree contains several generations of experimental scripts. They
are not interchangeable implementations.

| Family | Encoding or mechanism | Important distinction |
| --- | --- | --- |
| SAT | Rebuild a solver for each candidate span | Older non-incremental search |
| Incremental | Order-plus-mask encoding | Reuses the SAT solver and adds blocking clauses |
| Direct model | One-hot labels with pairwise, sequential, or cardinality-network constraints | Encoding changes clause structure, not the problem definition |
| Symmetric | Incremental encoding plus symmetry-breaking clauses | Must remain separate from the unrestricted model |
| Assumption | Fixed CNF with temporary assumptions | Does not permanently mutate the base CNF |
| CPLEX/Gurobi binary MIP | One-hot binary variables | Includes an all-different constraint in the legacy model |
| CPLEX CP | Integer label variables and native absolute-value constraints | Does not include the binary model's all-different constraint |

The method names `CMS` and `Glucose` in the legacy directories require audit:
the working implementations currently import `Cadical195` from PySAT. They
must not be described as CryptoMiniSat or Glucose experiments without evidence
of separate solver bindings.

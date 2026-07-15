# Reproducibility

## Environment

Use Python 3.10 or newer and install the base dependencies with:

```bash
python -m pip install -e ".[dev]"
```

CPLEX and Gurobi are optional commercial dependencies and require their own
local installations and licenses. Their versions must be recorded alongside
experiment results.

## Data

Instances are expected as square Matrix Market adjacency matrices. Keep the
original filename and record the commit or archive used to obtain the data.
The current checkout contains zero-byte `.mtx` placeholders, so published
tables cannot be regenerated from this checkout alone.

## Reporting

Record the method variant, Python version, PySAT and solver versions, machine
model, time limit, instance order, timeout status, and output CSV. Do not treat
a timeout as an optimal result. Before collecting tables, validate every
returned labeling independently with the radio constraint checker.

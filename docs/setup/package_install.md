---
title: "Local package install (required)"
---
> Last updated: {{ "now" | date: "%Y-%m-%d --- %H:%M:%S" (%Z)}}

The main script `scripts/calc_fib_indices.py` requires that you locally install the `top_fibers_pkg`.
To do this, change your current working directory to the `package/` directory inside of this repository and then run:

```bash
pip install -e .
```
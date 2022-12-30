---
title: "Understanding `top_fibers_pkg`"
last_modified: "2022-11-13"
---
> Last modified: {{ page.last_modified | date: "%Y-%m-%d"}}

[`top_fibers_pkg`](https://github.com/mr-devs/top-fibers/tree/main/package) is meant to be a locally maintained package that contains helpful data models, script helpers, and utility functions.
The intention is to keep things as clean and easy to maintain as possible.

There are three modules which are all heavily documented. 
For details, please see the code itself, however, below we list the modules and briefly describe the code contained within them.

- [`data_model.py`](https://github.com/mr-devs/top-fibers/blob/main/package/top_fibers_pkg/data_model.py): Contains classes that can read and process Twitter V1 tweet objects. These make code that extracts information from raw data much more robust and easier to understand (we hope).
- [`fib_helpers.py`](https://github.com/mr-devs/top-fibers/blob/main/package/top_fibers_pkg/fib_helpers.py): Contains helper functions utilized in the [`calc_fib_indices.py`](https://github.com/mr-devs/top-fibers/blob/main/scripts/calc_fib_indices.py) script.
- [`utils.py`](https://github.com/mr-devs/top-fibers/blob/main/package/top_fibers_pkg/utils.py): Contains general utility functions that may be utilized across various scripts. E.g., parsing command-line arguments, etc.
---
title: "Overview of how the code works"
last_modified: "2022-11-13"
---
> Last modified: {{ page.last_modified | date: "%Y-%m-%d"}}

There are three general processes that take place for the project to run.

### 1. Getting the data
The first step of the project is retrieving the data that is eventually processed to calculate the [FIB-index](../fib_index.md) values for all users.

Please see the [Data](../data.md) page for all details.

### 2. The FIB-index script
With the data gathered in the first process, we then must calculate each user's [FIB-index](../fib_index.md).
This is done with the [`calc_fib_indices.py`](https://github.com/mr-devs/top-fibers/blob/main/scripts/calc_fib_indices.py) script.

To understand how this code works please check out the [Understanding how the FIB script works](./fib_script.md) page.

### 3. The front end
Once the previous process has completed, we then consume the output of `calc_fib_indices.py` (see [this page for details](./fib_script.md)) and render it nicely on the [OSoMe website](https://osome.iu.edu/).

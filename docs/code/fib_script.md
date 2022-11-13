---
title: "Understanding how the FIB script works"
date: "2022-11-13"
last_modified: "2022-11-16"
---
> Last updated: {{ page.date | date: "%Y-%m-%d --- %H:%M:%S"}}
> Last modified: {{ page.last_modified | date: "%Y-%m-%d --- %H:%M:%S"}}

The [FIB-index](../fib_index.md) is a simple yet effective metric for estimating a social media user's influence within a misinformation network on a given platform.

To calculate FIB-indices, we have the [`calc_fib_indices.py`](https://github.com/mr-devs/top-fibers/blob/main/scripts/calc_fib_indices.py) script.
In this page, we attempt to provide a general overview of how the script works.

> Please see the [`calc_fib_indices.py`](https://github.com/mr-devs/top-fibers/blob/main/scripts/calc_fib_indices.py) script itself for indepth details, as the code is quite heavily documented.

From a high-level perspective, what this script attempts to do is read the input files line by line and extract only the information needed for FIB-index calculations.
Note that these files are are new-line delimited `.json.gz` format (see [Data](../data.md) for details).

Most importantly, we create a number of dictionaries that capture the number of retweets earned by users (usernames and user IDs) for original tweets, retweets, and quote tweets.
We create a list of retweet counts for each user in the data and then feed this list into the `calc_fib_index` function, which spits out that users FIB-index.
The total number of retweet counts earned by each user are calculated as well.

We do this for all users and create a pandas dataframe that is saved in `.parquet` format.
Each row represents one user and will include:
- total number of retweets earned
- FIB-index
- user ID
- username

Importantly, this code utilizes the locally installed [`top_fibers_pkg`](https://github.com/mr-devs/top-fibers/tree/main/package).
For details on this package, please checkout the [Understanding `top_fibers_pkg`](./top_fibers_pkg.md) page.
---
title: "Understanding how the FIB script works"
last_modified: "2022-11-13"
---
> Last modified: {{ page.last_modified | date: "%Y-%m-%d"}}

The [FIB-index](../fib_index.md) is a simple yet effective metric for estimating a social media user's influence within a misinformation network on a given platform.

To calculate FIB-indices, we have the [`calc_fib_indices.py`](https://github.com/mr-devs/top-fibers/blob/main/scripts/calc_fib_indices.py) script.
In this page, we attempt to provide a general overview of how the script works.

> Please see the [`calc_fib_indices.py`](https://github.com/mr-devs/top-fibers/blob/main/scripts/calc_fib_indices.py) script itself for indepth details, as the code is quite heavily documented.

From a high-level perspective, what this script does is take as input file paths which should contain data files that containt tweets _anywhere in its subdirectory_[^1].
This approach is taken because the standard output of Moe's Tavern returns a directory that contains various information we do not need for the [`calc_fib_indices.py`](https://github.com/mr-devs/top-fibers/blob/main/scripts/calc_fib_indices.py) script.
E.g., a file containing only tweet IDs is returned as well as logs and other unnecessary information.

From these directories, the full path to data files are returned and combined in a list.
Then, all data files are iterated through and processed line by line, extracting only the necessary information.

Most importantly, we create a number of dictionaries that capture the number of retweets earned by users (usernames and user IDs) for original tweets, retweets, and quote tweets.
We create a list of retweet counts for each user in the data and then feed this list into the `calc_fib_index` function, which spits out that users FIB-index.
The total number of retweet counts earned by each user are calculated as well.

We do this for all users and create a pandas dataframe that is saved in `.parquet` format.
Each row represents one user and will include:
- user ID
- username
- total number of retweets earned
- FIB-index

Importantly, this code utilizes the locally installed [`top_fibers_pkg`](https://github.com/mr-devs/top-fibers/tree/main/package).
For details on this package, please checkout the [Understanding `top_fibers_pkg`](./top_fibers_pkg.md) page.

[^1]: Note that these files are are new-line delimited `.json.gz` format (see [Data](../data.md) for details).
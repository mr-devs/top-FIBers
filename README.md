# top-fibers
Code to find and rank the top superspreaders of misinformation on Twitter using the FIB-index.

## Please checkout the documentation [here](https://www.matthewdeverna.com/top-FIBers/) for all details.

---


### See below for the general workflow.


> IMPORTANT:
> 1. **Must be in the repo root (`cd /home/data/apps/topfibers/repo`) or scripts will break.**
> 2. **Most commands below will require slight changes to capture the proper time period (YYYY_MM).**

1. **Move raw Twitter data to proper place**

After the raw files have been copied into the staging directory (`/home/data/apps/topfibers/moe_twitter_data`), we run the below script. This script moves `tweetContent/part-m-0000.gz` files to the platform-specific raw data directory (`/home/data/apps/topfibers/repo/data/raw`), updating the name to include the date.

```shell
python scripts/data_prep/move_twitter_raw.py
```

2. **Create symbolic links**

Now that the new data is in the proper place, we create a new directory that holds (via symbolic links pointing to the raw data folder) only the files we need for analysis in the next script.

```shell
python scripts/data_prep/create_data_file_symlinks.py -d /home/data/apps/topfibers/repo/data/raw/twitter/ -o /home/data/apps/topfibers/repo/data/symbolic_links/twitter -m 2022_02 -n 3
```
> If you do not pass the full path for the data/output directories, it will break the next script

3. **Generate FIB files**

Then we create the output files based on the FIB index. Note that there are two different scripts, one for each platform.

```shell
# For Twitter
python scripts/data_processing/calc_twitter_fib_indices.py -d /home/data/apps/topfibers/repo/data/symbolic_links/twitter/2022_10 -o /home/data/apps/topfibers/repo/data/derived/fib_results/twitter -m 2022_10 -n 3
```

or

```shell
# For Facebook
python scripts/data_processing/calc_crowdtangle_fib_indices.py -d /home/data/apps/topfibers/repo/data/symbolic_links/facebook/2022_01 -o /home/data/apps/topfibers/repo/data/derived/fib_results/facebook -m 2022_01 -n 3
```

> Note
> 1. The `YYYY_MM` date should be the same for the `-m` flag as well as the last dir of the `-d` input.



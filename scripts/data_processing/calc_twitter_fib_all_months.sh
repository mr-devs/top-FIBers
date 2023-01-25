#! bin/bash

# Purpose:
#   This is a simple script that calculates all of the FIB output files for Facebook data in all periods.
#   It is not intended to be used in the regular pipeline, but could be useful in the future if all files need to be
#   regenerated for some reason.
#
#   NOTE: The list of commands below will likely need to be updated for future calls and/or the script should be updated
#   to iterate through a list of YYYY_MM dates updating the -d and -m flag inputs.
#
# Inputs:
#   None
#
# Output:
#   All YYYY_MM_DD__fib_indices_<platform>.parquet and YYYY_MM_DD__top_spreader_posts_<platform>.parquet files
#   for all months
#
# How to call:
#   ```
#   cd /home/data/apps/topfibers/repo 
#   nohup python -u calc_twitter_fib_all_months.sh > logs/fib_tw_all.out 2>&1 &
#   ````
#
#   The above will write all output from all scripts to logs/fib_tw_all.out *as well as* the scripts own log file
#
# Author: Matthew DeVerna

cd /home/data/apps/topfibers/repo/

env_python=/home/data/apps/topfibers/repo/environments/env_code/bin/python

#python scripts/data_processing/calc_twitter_fib_indices.py -d /home/data/apps/topfibers/repo/data/symbolic_links/twitter/2022_04 -o /home/data/apps/topfibers/repo/data/derived/fib_results/twitter -m 2022_04 -n 3

#python scripts/data_processing/calc_twitter_fib_indices.py -d /home/data/apps/topfibers/repo/data/symbolic_links/twitter/2022_05 -o /home/data/apps/topfibers/repo/data/derived/fib_results/twitter -m 2022_05 -n 3

#python scripts/data_processing/calc_twitter_fib_indices.py -d /home/data/apps/topfibers/repo/data/symbolic_links/twitter/2022_06 -o /home/data/apps/topfibers/repo/data/derived/fib_results/twitter -m 2022_06 -n 3

#python scripts/data_processing/calc_twitter_fib_indices.py -d /home/data/apps/topfibers/repo/data/symbolic_links/twitter/2022_07 -o /home/data/apps/topfibers/repo/data/derived/fib_results/twitter -m 2022_07 -n 3

$env_python scripts/data_processing/calc_twitter_fib_indices.py -d /home/data/apps/topfibers/repo/data/symbolic_links/twitter/2022_08 -o /home/data/apps/topfibers/repo/data/derived/fib_results/twitter -m 2022_08 -n 3

$env_python scripts/data_processing/calc_twitter_fib_indices.py -d /home/data/apps/topfibers/repo/data/symbolic_links/twitter/2022_09 -o /home/data/apps/topfibers/repo/data/derived/fib_results/twitter -m 2022_09 -n 3

$env_python scripts/data_processing/calc_twitter_fib_indices.py -d /home/data/apps/topfibers/repo/data/symbolic_links/twitter/2022_10 -o /home/data/apps/topfibers/repo/data/derived/fib_results/twitter -m 2022_10 -n 3

#python scripts/data_processing/calc_twitter_fib_indices.py -d /home/data/apps/topfibers/repo/data/symbolic_links/twitter/2022_11 -o /home/data/apps/topfibers/repo/data/derived/fib_results/twitter -m 2022_11 -n 3

#python scripts/data_processing/calc_twitter_fib_indices.py -d /home/data/apps/topfibers/repo/data/symbolic_links/twitter/2022_12 -o /home/data/apps/topfibers/repo/data/derived/fib_results/twitter -m 2022_12 -n 3

#python scripts/data_processing/calc_twitter_fib_indices.py -d /home/data/apps/topfibers/repo/data/symbolic_links/twitter/2023_01 -o /home/data/apps/topfibers/repo/data/derived/fib_results/twitter -m 2023_01 -n 3

print("~~~~ Script complete ~~~~")

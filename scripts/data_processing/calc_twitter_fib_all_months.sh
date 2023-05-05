#! bin/bash

# Purpose:
#   This is a simple script that calculates all of the FIB output files for Facebook data in all periods.
#   It is not intended to be used in the regular pipeline, but could be useful in the future if all files need to be
#   regenerated for some reason.
#
#   IMPORTANT NOTE: This script will update ALL existing FIB output files. In theory, they should not change, however,
#   make sure you know what you are doing.
#
# Inputs:
#   None
#
# Output:
#   All YYYY_MM_DD__fib_indices_<platform>.parquet and YYYY_MM_DD__top_spreader_posts_<platform>.parquet files
#   for all months from 2022_01 to current month when script is executed.
#
# How to call:
#   ```
#   cd /home/data/apps/topfibers/repo 
#   nohup bash calc_twitter_fib_all_months.sh > logs/fib_tw_all.out 2>&1 &
#   ````
#
#   The above will write all output from all scripts to logs/fib_tw_all.out *as well as* the scripts own log file
#
# Author: Matthew DeVerna

# Get the current year and month
current_year=$(date +%Y)
current_month=$(date +%m)

# Define the start year and month
start_year=2022
start_month=01

# Create an empty array to hold the months
months=()

# Loop over the years and months and append to the array
for year in $(seq $start_year $current_year); do
    for month in $(seq -f "%02g" $start_month 12); do

        # Append the year-month string to the array
        months+=("${year}_${month}")

        # If we've reached the current month, exit the loop
        if [[ $year -eq $current_year && $month -eq $current_month ]]; then
            break 2
        fi
    done
    # Reset the start month to January after the first year
    start_month=01
done

env_python=/home/data/apps/topfibers/repo/environments/env_code/bin/python
script_path=/home/data/apps/topfibers/repo/scripts/data_processing/calc_twitter_fib_indices.py
data_path=/home/data/apps/topfibers/repo/data/symbolic_links/twitter
out_path=/home/data/apps/topfibers/repo/data/derived/fib_results/twitter
n_months=3

for month in "${months[@]}"; do
    $env_python $script_path -d $data_path/$month -o $out_path -m $month -n $n_months
done

echo ~~~ Script complete. ~~~

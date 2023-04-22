#!/bin/bash

# Download all Facebook data for each month between 2022-01-01 and the previous month,
# relative to when the script is executed.
#
# Notes:
#    - The script skips months for which data is already downloaded
#    - Must be run as the `truthy` user (to use the CrowdTangle API key, set as an environment variable)
#
# Author: Matthew DeVerna
# -------------------------

# Break if not in the project root
if [[ "$(pwd)" != "/home/data/apps/topfibers/repo" ]]; then
  echo "Script must be executed from /home/data/apps/topfibers/repo directory"
  exit 1
fi

# Set start_date to the beginning of the current month
start_date=2022-01-01

# Get the current date
now=$(date "+%Y-%m-%d")

# Set the end date to the beginning of the previous month
end_date=$(date -d "$now" +%Y-%m-01)
end_date=$(date -d "$end_date -1 month" +%Y-%m-%d)

# Set the directory to search for files
directory="/home/data/apps/topfibers/repo/data/raw/facebook"

# Get a list of files in the directory that match the desired format
files=$(find "$directory" -name '*fb_posts_w_links.jsonl.gzip' -type f)

# Loop through each month between start_date and end_date
while [ "$start_date" != "$end_date" ]; do

  # Extract the year and month from the start_date
  year_month=$(date -d "$start_date" "+%Y-%m")

  # Check if any files in the directory have the year_month in their filenames
  if echo "$files" | grep -q "$year_month"; then
    echo "Skipping $year_month because files already exist in $directory"
  else
    echo "Processing $year_month"
    #python -u scripts/data_collection/crowdtangle_dl_fb_links.py -d ./data/iffy_files/ -o /home/data/apps/topfibers/repo/data/raw/facebook -l $year_month -n 1
  fi

  # Move to the next month
  start_date=$(date -I -d "$start_date + 1 month")

done

echo "---- Script complete. ----"

#! bin/bash

# Purpose:
#   This is the master script that will be run each month for this project. It will activate all other
#   scripts in order, to ensure that each stop of the process happens properly.
#
#
# Inputs:
#   None
#
# Output:
#   Please see each of the scripts called below for their outputs/effect on the system.
#
# How to call:
#   ```
#   cd /home/data/apps/topfibers/repo 
#   nohup python -u monthly.sh > logs/YYYY-MM-DD__month_master_script.out 2>&1 &
#   ````
#
# Author: Matthew DeVerna

### Set variables for script
$PROJECT_ROOT=/home/data/apps/topfibers/repo
$PYTHON_ENV=/home/data/apps/topfibers/repo/environments/env_code/bin/python
$IFFY_FILES_DIR=/home/data/apps/topfibers/repo/data/iffy_files/
$LOG_DIR=/home/data/apps/topfibers/repo/logs


# Change dir to project repo root
cd $PROJECT_ROOT

### Download the latest Iffy news domains file
# Log file saved here: ./logs/iffy_update.log
$PYTHON_ENV scripts/data_collection/iffy_update.py -d $IFFY_FILES_DIR

### Download the Facebook data
# Log file saved here:
$PYTHON_ENV scripts/data_collection/crowdtangle_dl_fb_links.py

### Running the below script completes the following things:
#    1. Copies the latest Iffy news domains file to the Lisa-Moe shared drive
#    2. Creates a tavern job to pull the Twitter data for the past month
#    3. Copies those results to /home/data/apps/topfibers/moe_twitter_data on Lisa
bash scripts/data_collection/iffy_get_data.sh

### Move raw data to the proper place and format it correctly
# Log file saved here: ./logs/move_twitter_raw.log
$PYTHON_ENV scripts/data_prep/move_twitter_raw.py

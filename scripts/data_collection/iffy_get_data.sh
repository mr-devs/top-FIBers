#!/bin/bash

# Purpose:
#   This is a script that downloads the latest iffy list, then retrieve and save relevant raw twitter data from the past month.
#   The process goes between different servers(Lenny, Lisa, Moe) for convinience and load balancing.
#   
# Inputs:
#   None
#
# Configs:
#   fiber_home    :  topfibers project folder
#   tavern_job    :  moe's tavern is used for raw twitter data retrival, files first export from Moe to a shared path on Lisa, then transfered to Lenny.
#   KEY           :  the ssh key for Moe as appuser
#   iffy_filename :  filename for downloaded iffy list
#
# Output:
#   A folder named YYYY-MM containing data retrival results for the past month using the latest iffy list
#
# How to call:
#   ```
#   cd /home/data/apps/topfibers/repo
#   nohup ./scripts/data_collection/iffy_get_data.sh > ./logs/iffy_get_data.out 2>&1 &
#   ```
#
#   The above will output results to ${fiber_home}moe_twitter_data/YYYY-MM and save logs within /var/log/iffy_get_data.out
#
# Author: Nick Liu

year_month=$(date --date='last month' '+%Y-%m')
end_of_last_month=$(date -d "$(date +%Y-%m-01) -1 day" +%Y-%m-%d)
today="$(date +%Y-%m-%d)__"

fiber_home="/home/data/apps/topfibers/"
tavern_job="osome_swap/moe/jobs/top_fibers_data/" # relative path for the shared disk bewteen Lisa and Moe; prefix "/mnt/" -> Moe, prefix "/home/data/" -> Lisa
KEY=${HOME}/.ssh/id_rsa_moe
iffy_filename="iffy_list.txt"

# go to repo root
cd ${fiber_home}repo

# get latest iffy list
environments/env_code/bin/python scripts/data_collection/iffy_update.py -d "data/iffy_files"

# copy to Lisa-Moe shared drive
rsync -at data/iffy_files/${today}${iffy_filename} truthy@lisa.luddy.indiana.edu:/home/data/${tavern_job}${today}${iffy_filename}

#clean up tavern directory if exists
ssh -i ${KEY} appuser@moe-ln01.soic.indiana.edu "if [ -d "/mnt/${tavern_job}${year_month}" ]; then rm -Rf /mnt/${tavern_job}${year_month}; fi"

# create a tavern job
ssh -i ${KEY} appuser@moe-ln01.soic.indiana.edu "/home/appuser/truthy-cmd.sh get-tweets-with-meme -memes "/mnt/${tavern_job}${today}${iffy_filename}" -tstart "${year_month}-01" -tend "${end_of_last_month}" -tid false -ntweets 1000000 -outdir /mnt/${tavern_job}${year_month}/ -torf false"

#clean up raw teweet directory if exists
if [ -d "${fiber_home}moe_twitter_data/${year_month}" ]; then rm -Rf ${fiber_home}moe_twitter_data/${year_month}; fi

# copy results to Lenny:topfibers 
rsync -rt truthy@lisa.luddy.indiana.edu:/home/data/${tavern_job}${year_month} ${fiber_home}moe_twitter_data/

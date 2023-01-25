#!/bin/bash
year_month=$(date --date='last month' '+%Y-%m')
end_of_last_month=$(date -d "$(date +%Y-%m-01) -1 day" +%Y-%m-%d)

fiber_home="/home/data/apps/topfibers/"
tavern_job="osome_swap/moe/jobs/top_fibers_data/"
KEY=${HOME}/.ssh/id_rsa_moe

#check variables
echo "Start: " ${year_month}-01  "End: " ${end_of_last_month} "updating iffy"
echo "Fibers Home: " ${fiber_home}  
echo "Tavern Dir: " ${tavern_job}  
echo "Moe Key: "${KEY}
echo "rsync -at ${fiber_home}iffy_list truthy@lisa.luddy.indiana.edu:/home/data/${tavern_job}/"
echo "rsync -rt truthy@lisa.luddy.indiana.edu:/home/data/${tavern_job} ${fiber_home}moe_twitter_data/${year_month}"

# get latest iffy list
${fiber_home}repo/environments/env_code/bin/python /u/truthy/cronjobs/update_latestmonth_topfibers/iffy_update.py "${fiber_home}iffy_list"

# copy to Lisa-Moe shared drive
rsync -at ${fiber_home}iffy_list truthy@lisa.luddy.indiana.edu:/home/data/${tavern_job}/

# create a tavern job
ssh -i ${KEY} appuser@moe-ln01.soic.indiana.edu "/home/appuser/truthy-cmd.sh get-tweets-with-meme -memes "/mnt/${tavern_job}iffy_list" -tstart "${year_month}-01" -tend "${end_of_last_month}" -tid false -ntweets 1000000 -outdir /mnt/${tavern_job}${year_month}/ -torf false"

# copy results to Lenny:topfibers 
rsync -rt truthy@lisa.luddy.indiana.edu:/home/data/${tavern_job} ${fiber_home}moe_twitter_data/${year_month}
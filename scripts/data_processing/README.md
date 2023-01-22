# data_processing

Scripts that process the raw data in any way should be saved here.

### Scripts

- `calc_crowdtanlge_fib_all_months.sh` : runs `calc_crowdtangle_fib_indices.py` for all time periods
- `calc_crowdtangle_fib_indices.py` : creates two output files based on the FACEBOOK posts data for a given time period
    - A file containing the top 50 FIBers
    - A file containing all of their posts
- `calc_twitter_fib_all_months.sh` : runs `calc_twitter_fib_indices.py` for all time periods
- `calc_twitter_fib_indices.py` : creates two output files based on the TWITTER posts data for a given time period
    - A file containing the top 50 FIBers
    - A file containing all of their posts
- `count_num_posts.py` : count the number of posts that we have in all raw files contained in the data directory provided
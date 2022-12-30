#!/usr/bin/env python3
"""
Purpose:
    Calculate the FIB index for all users present in CrowdTangle files downloaded
    with INSERT DOWNLOAD SCRIPT NAME HERE.

Input:
    FULL PATH to the top-level directory that contains all CrowdTangle files.
    This script identifies the data files files from those directories by
    grabbing all paths that contain the MATCHING_STR constant defined below.

    NOTE:
    - Call the calc_crowdtangle_fib_indices.py -h flag to get input/flag details.
    - Input files contain Facebook posts.


Output:
    Two .parquet files containing:
    1. {YYYY_mm_dd}__fib_indices_crowdtangle.parquet: a pandas dataframe with the following columns:
        - user_id (str) : a unique Facebook user ID
        - fib_index (int) : a specific user's FIB index
        - total_reshares (int) : total number of reshares earned by user_id
    2. {YYYY_mm_dd}__top_spreader_posts_crowdtangle.parquet: a pandas dataframe with the following columns:
        - user_id (str) : a unique Facebook user ID
        - post_id (str) : a unique Facebook post ID
        - num_reshares (int) : the number of times post_id was reshared
        - timestamp (str) : timestamp when post was sent

    NOTE: YYYY_mm_dd will be representative of the machine's current date

What is the FIB-index?
    Please see our working paper for details.
    - https://arxiv.org/abs/2207.09524

Author: Matthew DeVerna
"""
### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Load Packages ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import datetime
import gzip
import json
import os

from collections import defaultdict
from top_fibers_pkg.data_model import FbIgPost
from top_fibers_pkg.dates import retrieve_paths_from_dir, get_earliest_date
from top_fibers_pkg.utils import parse_cl_args_fib
from top_fibers_pkg.fib_helpers import (
    create_userid_total_reshares,
    create_userid_reshare_lists,
    create_fib_frame,
    get_top_spreaders,
    create_top_spreader_df,
)

SCRIPT_PURPOSE = (
    "Return the FIB indices for all users present in the provided data "
    "as well as the posts sent by the worst misinformation spreaders."
)
MATCHING_STR = "*__fb_posts_w_links.jsonl.gzip"

# NOTE: Set the number of top ranked spreaders to select and which type
NUM_SPREADERS = 50
SPREADER_TYPE = "fib_index"  # Options: ["total_reshares", "fib_index"]

# Set the number of months to calculate the FIB index from
NUM_MONTHS = 3

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Set Functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def extract_data_from_files(data_files, earliest_date_tstamp):
    """
    Extract necessary data from the list of input files.

    Parameters:
    -----------
    - data_files (list) : list of full paths to data files to parse
    - earliest_date_tstamp (timestamp) : the earliest date from which to consider
        data for calculating FIB indices

    Returns:
    -----------
    - userid_username (dict) : maps user IDs to usernames
    - userid_postids (dict) : maps user IDs to a set of (str) post IDs
    - postid_timestamp (dict) : maps post IDs to (str) timestamps
    - postid_num_reshares (dict) : maps post IDs to number of reshares (int)

    Exceptions:
    -----------
    TypeError
    """
    if not isinstance(data_files, list):
        raise TypeError("`data_files` must be a list!")

    # Initialize data objects to populate
    userid_username = dict()
    userid_postids = defaultdict(set)

    postid_timestamp = dict()
    postid_num_reshares = defaultdict(int)

    print("Begin extracting data.")
    try:
        for file in data_files:
            print(f"\t- Processing: {os.path.basename(file)} ...")
            with gzip.open(file, "rb") as f:
                for line in f:
                    post_obj = FbIgPost(json.loads(line.decode()))
                    if not post_obj.is_valid():
                        continue

                    post_id = post_obj.get_post_ID()
                    timestamp_str = post_obj.get_post_time(timestamp=True)
                    timestamp = datetime.datetime.fromtimestamp(
                        int(timestamp_str)
                    ).timestamp()
                    # Skip anything posted before the earliest date
                    if timestamp < earliest_date_tstamp:
                        continue
                    user_id = post_obj.get_user_ID()
                    username = post_obj.get_user_handle()
                    reshare_count = post_obj.get_reshare_count()
                    if reshare_count is None:
                        reshare_count = 0

                    postid_num_reshares[post_id] = reshare_count
                    postid_timestamp[post_id] = timestamp_str
                    userid_username[user_id] = username
                    userid_postids[user_id].add(post_id)

        num_posts = len(postid_num_reshares.keys())
        num_users = len(userid_username.keys())
        print(f"Total Posts Ingested = {num_posts}")
        print(f"Total Number of Users = {num_users}")

        return (
            userid_username,
            dict(userid_postids),
            postid_timestamp,
            dict(postid_num_reshares),
        )

    except Exception as e:
        raise Exception(e)


# Execute the program
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    # Parse input flags
    args = parse_cl_args_fib(SCRIPT_PURPOSE)
    data_dirs = args.data
    output_dir = args.out_dir
    month_calculated = args.month_calculated
    if output_dir is None:
        output_dir = "."

    # Retrieve all paths to data files
    print("Data will be extracted from here:")
    data_files = []
    for data_dir in data_dirs:
        print(f"\t- {data_dir}")
        lst_data_files = retrieve_paths_from_dir(data_dir, matching_str=MATCHING_STR)
        data_files.extend(lst_data_files)
    num_files = len(data_files)
    print(f"\nNum. files to process: {num_files}\n")

    # Get the first date of
    earliest_date_tstamp = get_earliest_date(
        months_earlier=NUM_MONTHS, as_timestamp=True, month_calculated=month_calculated
    )
    (
        userid_username,
        userid_postids,
        postid_timestamp,
        postid_num_reshares,
    ) = extract_data_from_files(data_files, earliest_date_tstamp)

    print("Creating output dataframes...")
    userid_total_reshares = create_userid_total_reshares(
        postid_num_reshares, userid_postids
    )
    userid_reshare_lists = create_userid_reshare_lists(
        postid_num_reshares, userid_postids
    )
    fib_frame = create_fib_frame(
        userid_reshare_lists, userid_username, userid_total_reshares
    )

    print("Top spreader information:")
    print(f"\t- Num. spreaders to select   : {NUM_SPREADERS}")
    print(f"\t- Type of spreaders to select: {SPREADER_TYPE}")
    top_spreaders = get_top_spreaders(fib_frame, NUM_SPREADERS, SPREADER_TYPE)
    top_spreader_df = create_top_spreader_df(
        top_spreaders, userid_postids, postid_num_reshares, postid_timestamp
    )

    fib_frame = fib_frame.sort_values("fib_index", ascending=False).reset_index(
        drop=True
    )
    top_spreader_df = top_spreader_df.sort_values(
        "num_reshares", ascending=False
    ).reset_index(drop=True)

    # Save files
    print("Saving data...")
    today = datetime.datetime.now().strftime("%Y_%m_%d")
    output_fib_fname = os.path.join(
        output_dir, f"{today}__fib_indices_crowdtangle.parquet"
    )
    output_rt_fname = os.path.join(
        output_dir, f"{today}__top_spreader_posts_crowdtangle.parquet"
    )
    fib_frame.to_parquet(output_fib_fname, index=False, engine="pyarrow")
    top_spreader_df.to_parquet(output_rt_fname, index=False, engine="pyarrow")

    print("Script Complete.")

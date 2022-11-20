#!/usr/bin/env python3
"""
Purpose:
    Calculate the FIB index for all users present in tweet files output by Moe's
    Tavern.

Input:
    FULL PATH to the top-level directories created by a Moe's Tavern query.
    This script parses the actual tweetContent files (part-m-XXXXX) files from
    those directories by grabbing all paths that contain the MATCHING_STR constant
    defined below.

    NOTE: Call the calc_fib_indices.py -h flag to get input/flag details.

Output:
    Two .parquet files containing:
    1. {YYYY_mm_dd}__fib_indices.parquet: a pandas dataframe with the following columns:
        - user_id (str) : a unique Twitter user ID
        - fib_index (int) : a specific user's FIB index
        - total_retweets (int) : a specific user's FIB index

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

import pandas as pd

from collections import defaultdict, Counter
from top_fibers_pkg.data_model import Tweet_v1
from top_fibers_pkg import calc_fib_index, parse_cl_args, retrieve_paths_from_dir

SCRIPT_PURPOSE = "Calculate FIB indices for all users present in the provided data."
MATCHING_STR = "part*.gz"

# NOTE: Take the top 50 FIBers AND top 50 most retweeted users (so we'll get more than 50 accounts)
NUM_TOP_USERS = 50

### ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Set Functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def load_tweets(data_files):
    """
    Load tweet data into three dictionaries that include only the
    needed information: user IDs/screennames and retweet counts

    Parameters:
    -----------
    - data_files(list) : a list of paths to files

    Returns:
    -----------
    - tweetid_max_rts (dict) : {tweet_id_str : max number of retweets in data}
    - userid_tweetids (dict) : {userid_x : set([tweetids sent by userid_x])}
    - userid_username (dict) : {userid : username}
        NOTE: the username will be the last one encountered, which will also be
        the most recent.

    Exceptions:
    -----------
    - Exception, TypeError
    """
    if not isinstance(data_files, list):
        raise TypeError("`data_files` must be a list!")
    if not all(isinstance(path, str) for path in data_files):
        raise TypeError("All `data_files` must be a string!")

    tweetid_timestamp = dict()
    tweetid_max_rts = defaultdict(int)
    userid_tweetids = defaultdict(set)
    userid_username = dict()

    try:
        for file in data_files:
            print(f"Loading tweets from file: {file}...")
            with gzip.open(file, "rb") as f:
                for line in f:
                    tweet = Tweet_v1(json.loads(line.decode()))

                    if not tweet.is_valid():
                        print("Skipping invalid tweet!!")
                        print("-" * 50)
                        print(tweet.post_object)
                        print("-" * 50)
                        continue

                    # Parse the base-level tweet
                    tweet_id = tweet.get_post_ID()
                    timestamp = tweet.get_post_time(timestamp=True)
                    user_id = tweet.get_user_ID()
                    username = tweet.get_user_handle()

                    rt_count = tweet.get_reshare_count()
                    prev_rt_val = tweetid_max_rts[tweet_id]
                    if prev_rt_val > rt_count:
                        rt_count = prev_rt_val

                    # Store the data
                    tweetid_timestamp[tweet_id] = timestamp
                    tweetid_max_rts[tweet_id] = rt_count
                    userid_tweetids[user_id].add(tweet_id)
                    userid_username[user_id] = username

                    # Handle retweets
                    if tweet.is_retweet:
                        tweet_id = tweet.retweet_object.get_post_ID()
                        timestamp = tweet.retweet_object.get_post_time(timestamp=True)
                        user_id = tweet.retweet_object.get_user_ID()
                        username = tweet.retweet_object.get_user_handle()

                        rt_count = tweet.retweet_object.get_reshare_count()
                        prev_rt_val = tweetid_max_rts[tweet_id]
                        if prev_rt_val > rt_count:
                            rt_count = prev_rt_val

                        # Store the data
                        tweetid_timestamp[tweet_id] = timestamp
                        tweetid_max_rts[tweet_id] = rt_count
                        userid_tweetids[user_id].add(tweet_id)
                        userid_username[user_id] = username

                    # Handle quotes
                    if tweet.is_quote:
                        tweet_id = tweet.quote_object.get_post_ID()
                        timestamp = tweet.quote_object.get_post_time(timestamp=True)
                        user_id = tweet.quote_object.get_user_ID()
                        username = tweet.quote_object.get_user_handle()

                        rt_count = tweet.quote_object.get_reshare_count()
                        prev_rt_val = tweetid_max_rts[tweet_id]
                        if prev_rt_val > rt_count:
                            rt_count = prev_rt_val

                        # Store the data
                        tweetid_timestamp[tweet_id] = timestamp
                        tweetid_max_rts[tweet_id] = rt_count
                        userid_tweetids[user_id].add(tweet_id)
                        userid_username[user_id] = username

        num_tweets = len(tweetid_max_rts.keys())
        num_users = len(userid_tweetids.keys())
        print(f"Total Tweets Ingested = {num_tweets}")
        print(f"Total Number of Users = {num_users}")

        return dict(tweetid_max_rts), dict(userid_tweetids), userid_username, tweetid_timestamp

    # Raise this error if something weird happens loading the data
    except Exception as e:
        raise Exception(e)


def create_userid_rt_counts(tweetid_max_rts, userid_tweetids):
    """
    Create a dictionary that takes the following form:
    - keys = user id strings
    - values = list of max retweets earned in our data for any tweet sent by them

    Parameters:
    -----------
    - tweetid_max_rts (dict) : {tweet_id_str : max number of retweets in data}
    - userid_tweetids (dict) : {userid_x : set([tweetids sent by userid_x])}

    Returns:
    -----------
    - userid_rt_count_lists (dict) : {userid_x : list([rt count (int) for each tweetid sent by userid_x])}
    - userid_rt_counts (dict) : {userid_x : total rts earned by userid_x}

    Exceptions:
    -----------
    - Exception, TypeError
    """
    if not isinstance(tweetid_max_rts, dict):
        raise TypeError("`tweetid_max_rts` must be a dict!")
    if not isinstance(userid_tweetids, dict):
        raise TypeError("`userid_tweetids` must be a dict!")

    try:
        userid_rt_count_lists = defaultdict(list)
        userid_rt_counts = Counter()
        for userid, tweetids in userid_tweetids.items():
            for tweetid in tweetids:
                num_rts = tweetid_max_rts[tweetid]
                userid_rt_count_lists[userid].append(num_rts)
                userid_rt_counts[userid] += num_rts
        return userid_rt_count_lists, dict(userid_rt_counts)

    except Exception as e:
        raise Exception(e)


def create_fib_frame(userid_rt_count_lists, userid_username):
    """
    Create a dataframe where each row contains a single users identification
    information and FIB-index.

    Parameters:
    -----------
    - userid_rt_count_lists (dict) : {userid_x : list([rt count (int) for each tweetid sent by user_x])}
    - userid_username (dict) : {userid : username}

    Returns:
    -----------
    - fib_frame (pandas.DataFrame) : a dataframe containing the following columns:
        - user_id (str) : the user's Twitter user ID
        - username (str) : the user's username/handle
        - fib_index (int) : the fib index for that user (sorted in descending order)

    Exceptions:
    -----------
    - Exception, TypeError
    """
    if not isinstance(userid_rt_count_lists, dict):
        raise TypeError("`userid_rt_count_lists` must be a dict!")

    user_records = []
    try:
        for userid, rt_cnt_list in userid_rt_count_lists.items():
            user_records.append(
                {
                    "user_id": userid,
                    "username": userid_username[userid],
                    "fib_index": calc_fib_index(rt_cnt_list),
                }
            )

        fib_frame = pd.DataFrame.from_records(user_records)

        return fib_frame

    except Exception as e:
        raise Exception(e)


# Execute the program
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    # Parse input flags
    args = parse_cl_args(SCRIPT_PURPOSE)
    data_dirs = args.data
    output_dir = args.out_dir
    if output_dir is None:
        output_dir = "."

    # Retrieve all paths to data files
    data_files = []
    for data_dir in data_dirs:
        lst_data_files = retrieve_paths_from_dir(data_dir, matching_str=MATCHING_STR)
        data_files.extend(lst_data_files)
    
    print("Data files that will be processed:")
    for f in data_files:
        print(f"\t- {f}")

    # Wrangle data and calculate FIB indices
    tweetid_max_rts, userid_tweetids, userid_username, tweetid_timestamp = load_tweets(data_files)
    userid_rt_count_lists, userid_rt_counts = create_userid_rt_counts(
        tweetid_max_rts, userid_tweetids
    )
    fib_frame = create_fib_frame(userid_rt_count_lists, userid_username)
    userid_rt_counts_frame = pd.DataFrame.from_records(
        list(userid_rt_counts.items()), columns=["user_id", "total_retweets"]
    )
    userid_rt_counts_frame.sort_values(
        by="total_retweets", ascending=False, inplace=True
    )
    fib_frame = fib_frame.merge(userid_rt_counts_frame, on="user_id")
    
    # Get top 50 users with most total retweets
    fib_frame.sort_values(by="total_retweets", ascending=False, inplace=True)
    top_50_rts = list(fib_frame["user_id"].head(NUM_TOP_USERS))

    # Get top 50 users with the highest FIB indices
    fib_frame.sort_values(by="fib_index", ascending=False, inplace=True)
    top_50_fibers = list(fib_frame["user_id"].head(NUM_TOP_USERS))

    # Combine them into one set and create records for each tweet
    hitlist = set(top_50_fibers + top_50_rts)
    hitlist_records = []
    for user_id in hitlist:
        user_tweetids = userid_tweetids[user_id]
        for tid in user_tweetids:
            hitlist_records.append({
                "user_id" : user_id,
                "tweet_id" : tid,
                "num_rts" : tweetid_max_rts[tid],
                "timestamp" : tweetid_timestamp[tid],
            })
    hitlist_df = pd.DataFrame.from_records(hitlist_records)

    # Save files
    today = datetime.datetime.now().strftime("%Y_%m_%d")
    output_fib_fname = os.path.join(output_dir, f"{today}__fib_indices.parquet")
    output_rt_fname = os.path.join(output_dir, f"{today}__hitlist_rts.parquet")
    fib_frame.to_parquet(output_fib_fname, index=False, engine="pyarrow")
    hitlist_df.to_parquet(output_rt_fname, index=False, engine="pyarrow")

    print("Script Complete.")

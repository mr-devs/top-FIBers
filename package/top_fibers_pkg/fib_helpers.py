"""
A collection of functions that are utilized in the calc_fib_indices.py script.
"""
import os
import fnmatch

def calc_fib_index(rt_counts):
    """
    Calculate a user's FIB-index based a list of the retweet counts they earned.

    Parameters:
    -----------
    - rt_counts (list) : list of retweet count values for retweets sent by a user

    Return:
    -----------
    - fib_position (int) : a user's FIB index

    Errors:
    -----------
    - TypeError
    """
    if not isinstance(rt_counts, list):
        raise TypeError("`rt_counts` must be a list!")

    rt_counts.sort()
    for fib_position in range(1, len(rt_counts) + 1)[::-1]:
        if rt_counts[-fib_position] >= fib_position:
            return fib_position

    # If the above criteria is never met, we return the fib_position as zero
    fib_position = 0
    return fib_position


def retrieve_paths_from_dir(dir_path, matching_str="part*.gz"):
    """
    Return the full path of files in `dir_path` that match `matching_str`

    Parameters:
    -----------
    dir_path (str) : full path to a top-level directory
    matching_str (str) : files that match this string within `dir_path` will be
        returned. Matching done with fnmatch.fnmatch() so wildcards are allowed.
        Default is "part*.gz"
    
    Returns:
    -----------
    data_paths (list) : a list of all full file paths to any file that matches
        `matching_str`
    """
    if not isinstance(dir_path, str):
        raise Exception(f"`dir_path` must be a string. You passed a {type(dir_path)}")

    data_paths = []
    for root, subdirs, files in os.walk(dir_path):
        for filename in files:
            if fnmatch.fnmatch(filename, matching_str):
                data_paths.append(os.path.join(root,filename))
    
    return data_paths
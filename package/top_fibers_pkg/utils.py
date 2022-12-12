"""
Some simple utility functions used throughout the project.
"""
import argparse
import datetime
import fnmatch
import os

from dateutil.relativedelta import relativedelta


def parse_cl_args_fib(script_purpose=""):
    """
    Read command line arguments for the scripts that calculate FIB indices.
        - top-fibers/scripts/calc_crowdtangle_fib_indices.py
        - top-fibers/scripts/calc_twitter_fib_indices.py

    Parameters:
    --------------
    - script_purpose (str) : Purpose of the script being utilized. When printing
        script help message via `python script.py -h`, this will represent the
        script's description. Default = "" (an empty string)

    Returns
    --------------
    None

    Exceptions
    --------------
    None
    """
    print("Parsing command line arguments...")

    # Initiate the parser
    parser = argparse.ArgumentParser(description=script_purpose)

    # Add long and short argument
    msg = (
        "One or more paths to directories that contain data files with tweets/posts. "
        "Will recursively iterate through all subdirectors to find files that match "
        "the MATCHING_STR parameter specified within that script. "
        "Tweet/post files should be new-line delimited json.gz"
    )
    parser.add_argument(
        "-d",
        "--data",
        metavar="Data",
        nargs="+",
        help=msg,
        required=True,
    )
    parser.add_argument(
        "-o",
        "--out-dir",
        metavar="Output dir",
        help="Directory where you'd like to save the output data",
        required=True,
    )

    # Read parsed arguments from the command line into "args"
    args = parser.parse_args()

    return args


def parse_cl_args_ct_dl(script_purpose=""):
    """
    Read command line arguments for the script that downloads Facebook posts from
    CrowdTangle.
        - top-fibers/data_collection/crowdtangle_dl_fb_links.py

    Parameters:
    --------------
    - script_purpose (str) : Purpose of the script being utilized. When printing
        script help message via `python script.py -h`, this will represent the
        script's description. Default = "" (an empty string)

    Returns
    --------------
    None

    Exceptions
    --------------
    None
    """
    print("Parsing command line arguments...")

    # Initiate the parser
    parser = argparse.ArgumentParser(description=script_purpose)

    # Add long and short argument
    msg = (
        "Full path to a file with one domain on each line. Posts will be downloaded "
        "that include at least one of these domains"
    )
    parser.add_argument(
        "-d",
        "--domains-file",
        metavar="Domains file",
        help=msg,
        required=True,
    )
    parser.add_argument(
        "-o",
        "--out-dir",
        metavar="Output dir",
        help="Directory where you'd like to save the output data",
        required=True,
    )

    # Read parsed arguments from the command line into "args"
    args = parser.parse_args()

    return args


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
    for root, _, files in os.walk(dir_path):
        for filename in files:
            if fnmatch.fnmatch(filename, matching_str):
                data_paths.append(os.path.join(root, filename))

    return data_paths


def get_dict_val(dictionary: dict, key_list: list = []):
    """
    Return `dictionary` value at the end of the key path provided in `key_list`.
    Indicate what value to return based on the key_list provided. For example, from
    left to right, each string in the key_list indicates another nested level further
    down in the dictionary. If no value is present, `None` is returned.
    Parameters:
    ----------
    - dictionary (dict) : the dictionary object to traverse
    - key_list (list) : list of strings indicating what dict_obj
        item to retrieve
    Returns:
    ----------
    - key value (if present) or None (if not present)
    Raises:
    - TypeError
    Examples:
    ---------
    # Create dictionary
    dictionary = {
        "a" : 1,
        "b" : {
            "c" : 2,
            "d" : 5
        },
        "e" : {
            "f" : 4,
            "g" : 3
        },
        "h" : 3
    }
    ### 1. Finding an existing value
    # Create key_list
    key_list = ['b', 'c']
    # Execute function
    get_dict_val(dictionary, key_list)
    # Returns
    2
    ~~~
    ### 2. When input key_path doesn't exist
    # Create key_list
    key_list = ['b', 'k']
    # Execute function
    value = get_dict_val(dictionary, key_list)
    # Returns NoneType because the provided path doesn't exist
    type(value)
    NoneType
    """
    if not isinstance(dictionary, dict):
        raise TypeError("`dictionary` must be of type `dict`")

    if not isinstance(key_list, list):
        raise TypeError("`key_list` must be of type `list`")

    retval = dictionary
    for k in key_list:

        # If retval is not a dictionary, we're going too deep
        if not isinstance(retval, dict):
            return None

        if k in retval:
            retval = retval[k]

        else:
            return None
    return retval


def load_lines(file_path):
    """
    Load the lines of a file into a list, stripping unwanted content from the
    rightside of each line (e.g., \n, tabs, etc.)

    Parameters:
    ------------
    - file_path (str): path to the file you want to load

    Returns:
    ------------
    - lines (list[str]): list where each item represents one line from `file_path`
        with newline characters, tabs, and other unwanted content removed.

    Exception:
    ------------
    TypeError
    """
    if not isinstance(file_path, str):
        raise TypeError("file_path must be a string")

    with open(file_path, "r") as f:
        return [line.rstrip() for line in f]


def get_start_and_end_dates(num_months, offset):
    """
    Return start and end dates (in datetime objects) based on the inputs.

    Parameters:
    ------------
    - num_months (int): the number of continuous months to encapsulate capture
        between start_date and end_date
    - offset (int): number of months to offset from the current month. Utilized
        to set the end date month.
        - If offset = 0: end date month is datetime.datetime.now().month
        - If offset = -1: end date month is datetime.datetime.now().month - 1 (previous month)
        - If offset = 1: end date month is datetime.datetime.now().month + 1 (following month)

    Returns:
    ------------
    (start_date, end_date) where...
    - start_date (datetime.date): will always be the first day of the month
    - end_date (datetime.date): will always be the last day of that month
    """
    if not isinstance(num_months, int):
        raise ValueError(
            "`num_months` must be an integer. "
            f"Currently its type is: {type(num_months)}"
        )
    if not isinstance(offset, int):
        raise ValueError(
            "`offset` must be an integer. " f"Currently its type is: {type(offset)}"
        )

    # Get current date as anchor point in time
    now = datetime.datetime.now()

    # Get date, offset by the correct number of months (accounts for year change)
    # Add one to offset so it's easier to get end_date
    offset_dt = now + relativedelta(months=offset + 1)
    end_date = offset_dt - datetime.timedelta(days=offset_dt.day)
    end_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = end_date - relativedelta(months=num_months - 1)
    start_date = start_date.replace(day=1)
    end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=0)
    return (start_date, end_date)

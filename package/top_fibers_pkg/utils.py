"""
Some simple utility functions used throughout the project.
"""
import argparse


def parse_cl_args_symlinks(script_purpose=""):
    """
    Read command line arguments for the symlink creation script.
        - top-fibers/scripts/create_data_file_symlinks.py

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
        "the MATCHING_STR parameter specified within the script. "
        "Tweet/post files should be new-line delimited json.gz"
    )
    parser.add_argument(
        "-d",
        "--data",
        metavar="Data",
        help="Data directory that contains the raw data files",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--out-dir",
        metavar="Output dir",
        help="Directory where you'd like to save the output data",
        required=True,
    )
    parser.add_argument(
        "-m",
        "--month-calculated",
        metavar="Month calculated",
        help="The month for which you'd like to calculate FIB indices (YYYY-MM)",
        required=True,
    )
    parser.add_argument(
        "-n",
        "--num-months",
        metavar="Number of months considered",
        help="The number of months to consider (e.g., input 3 to consider three months)",
        required=True,
    )

    # Read parsed arguments from the command line into "args"
    args = parser.parse_args()

    return args


def parse_cl_args_fib(script_purpose=""):
    """
    Read command line arguments for the following scripts.
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
    parser.add_argument(
        "-d",
        "--data",
        metavar="Data",
        help="Full path to the data you'd like to calculate FIB indices for",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--out-dir",
        metavar="Output dir",
        help="Directory where you'd like to save the output data",
        required=True,
    )
    parser.add_argument(
        "-m",
        "--month-calculated",
        metavar="Month calculated",
        help="The month for which you'd like to calculate FIB indices (YYYY-MM)",
        required=True,
    )
    parser.add_argument(
        "-n",
        "--num-months",
        metavar="Number of months considered",
        help="The number of months to consider (e.g., input 3 to consider three months)",
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

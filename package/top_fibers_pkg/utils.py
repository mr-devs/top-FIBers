"""
Some simple utility functions used throughout the project.
"""
import argparse
import fnmatch
import os


def parse_cl_args(script_purpose):
    """Read Command Line Arguments."""
    print("Parsing command line arguments...")

    # Initiate the parser
    parser = argparse.ArgumentParser(description=script_purpose)

    # Add long and short argument
    msg = (
        "One or more paths to directories that contain tweet files. "
        "Should be the top-level directory containing output from Moe's Tavern. "
        "Tweet content files in the sub directories of these directories should "
        "be new-line delimited json.gz"
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
        required=False,
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

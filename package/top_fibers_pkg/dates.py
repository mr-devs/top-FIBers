"""
Functions for working with dates.
"""
import datetime
import fnmatch
import os

from dateutil.relativedelta import relativedelta


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


def get_earliest_date(months_earlier, as_timestamp=False, month_calculated=None):
    """
    Return the earliest date allowed based on month_calculated and months_earlier.
    Will be the first day of the month based on the number of months_earlier
    than the base date (i.e., month_calculated - months_earlier).

    Example:
    months_earlier = 3
    month_calculated = "2022-12"
    earliest_date = get_earliest_date(months_earlier, as_timestamp=False, month_calculated=month_calculated)
    print(earliest_date)
    >>> 2022-08-01 00:00:00

    Parameters:
    -----------
    - months_earlier (int): the number of months earlier from which to set the earliest date
    - as_timestamp (bool) : if True, return as timestamp; if False, return as datetime object
        default = False
    - month_calculated (str) : the anchor date from which to identify the earliest date.
        Format must be "%Y-%m"

    Return:
    -----------
    - earliest_date (datetime.datetime or timestamp) : the earliest date based on the
        months_earlier input. Will always be the first day of that month.

    Exception:
    -----------
    TypeError
    """
    if not isinstance(as_timestamp, bool):
        raise TypeError(
            "`as_timestamp` must be a boolean. "
            f"Currently its type is: {type(as_timestamp)}"
        )
    if not isinstance(month_calculated, str):
        raise TypeError(
            "`month_calculated` must not be None. "
            f"Input should be a string like: YYYY-MM"
        )
    if not isinstance(months_earlier, int):
        raise TypeError(
            "`months_earlier` must be an integer. "
            f"Currently its type is: {type(months_earlier)}"
        )

    # Use month_calculated as anchor point in time
    month_calculated_dt = datetime.datetime.strptime(month_calculated, "%Y-%m")

    # Get date, offset by the input number of months_earlier (accounts for year change)
    offset_dt = month_calculated_dt - relativedelta(months=months_earlier)

    # Use year and month to create datetime object for earliest date allowed
    earliest_dt = datetime.datetime(year=offset_dt.year, month=offset_dt.month, day=1)

    if as_timestamp:
        return earliest_dt.timestamp()
    return earliest_dt

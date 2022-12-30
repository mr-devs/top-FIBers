"""
Purpose:
    This script creates a directory of symbolic links to both Twitter and Facebook
    raw data files. The directory name and files chosen are based on the inputs.

Inputs:
    - Those loaded by top_fibers_pkg.utils.parse_cl_args_symlinks

Outputs:
    Creates a directory (named based on base date; format "%Y_%m") with the
    following contents:
    |- YYYY_MM
    |   |- sym_link_to_raw_file_1
    |   |- sym_link_to_raw_file_2
    |   |- ...
"""
import datetime
import glob
import os

from top_fibers_pkg.utils import parse_cl_args_symlinks, get_logger
from top_fibers_pkg.dates import get_earliest_date

SCRIPT_PURPOSE = "Create symbolic links for the period specified"
LOG_DIR = "/data_volume/top-fibers/logs"
LOG_FNAME = "data_file_symlinks.log"


def get_symlink_tuples(files, start, end, output_dir_w_month):
    """
    Create a list of (source, new_location) tuples.
    """
    files_to_symlink = []
    for file in files:
        # Example basenames:
        #  Facebook: 2022-04-01--2022-04-30__fb_posts_w_links.jsonl.gzip
        #  Twitter : 2022-11-01__tweets_w_links.jsonl.gzip
        basename = os.path.basename(file)
        dates_and_suffix = basename.split("__")
        start_date = dates_and_suffix[0].split("--")[0]
        date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        if start <= date_obj < end:
            new_location = os.path.join(output_dir_w_month, basename)
            sym_tuple = (file, new_location)
            files_to_symlink.append(sym_tuple)
    return files_to_symlink


def create_sym_links(file_tuples):
    """
    Create symbolic links based on the list of tuples provide
    """
    if not isinstance(file_tuples, list):
        raise TypeError(
            f"`files_tuple` must be a list. " f"Currently, type is: {type(file_tuples)}"
        )

    for source, new_location in file_tuples:
        logger.info("Creating following symlink:")
        logger.info(f"\tSource      : {source}")
        logger.info(f"\tNew Location: {new_location}")
        os.symlink(source, new_location)
    logger.info("All symbolic links created.")


if __name__ == "__main__":
    script_name = os.path.basename(__file__)
    logger = get_logger(LOG_DIR, LOG_FNAME, script_name=script_name)
    logger.info("-" * 50)
    logger.info(f"Begin script: {script_name}")

    args = parse_cl_args_symlinks(SCRIPT_PURPOSE, logger)
    data_path = args.data
    output_dir = args.out_dir
    month_calculated = args.month_calculated
    num_months = int(args.num_months)

    # Get start and end date based on input date
    start = get_earliest_date(
        months_earlier=num_months, as_timestamp=False, month_calculated=month_calculated
    )
    end = datetime.datetime.strptime(month_calculated, "%Y_%m")
    logger.info(f"Start date: {start}")
    logger.info(f"End date: {end}")

    # Create output dir if it doesn't exist
    output_dir_w_month = os.path.join(output_dir, month_calculated)
    if not os.path.exists(output_dir_w_month):
        os.makedirs(output_dir_w_month)

    files = glob.glob(os.path.join(data_path, "*.gzip"))
    files_to_symlink = get_symlink_tuples(files, start, end, output_dir_w_month)
    create_sym_links(files_to_symlink)

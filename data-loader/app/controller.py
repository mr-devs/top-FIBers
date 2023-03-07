import os
import pandas as pd
import re
import datetime
import logging
from database_functions import reports, fib_indices, posts, reshares
import traceback


root_dir = "../../data/fib_results/"
FIB_INDICES = 'fib_indices'
TOP_SPREADERS = 'top_spreader'
N_ROWS = 50

logger = logging.getLogger(__name__)

def read_files(read_dir, platform, selected_month):
    """
    Read the config file and insert the data to database.
    """
    logger.info("Found the data directory on that day!")
    list_dir = os.listdir(os.path.join(read_dir, selected_month +'/'))
    if len(list_dir) > 0:
        file_date = extract_date_convert_datetime(list_dir[0])
        if reports.check_report_already_added(file_date, selected_month, platform):
            report_id = reports.add_reports(file_date, selected_month, platform)
            for file in list_dir:
                try:
                    local_dir = os.path.join(os.path.join(read_dir, selected_month + '/'), file)
                    if FIB_INDICES in file:
                        logger.info("Loading fib indices file for the {}", selected_month)
                        df_fib_indices = pd.read_parquet(local_dir)
                        temp_df = df_fib_indices.head(N_ROWS)
                        for index,row in temp_df.iterrows():
                            try:
                                fib_indices.add_fib_indices(row.user_id, report_id.get('id'), row.fib_index,row.total_reshares, row.username, platform)
                            except Exception as err:
                                traceback.print_tb(err.__traceback__)
                                logger.error("Error in adding data to fib indices")
                    elif TOP_SPREADERS in file:
                        logger.info("Loading top spreader file for the {}", selected_month)
                        df_top_spreaders = pd.read_parquet(local_dir)
                        for index,row in df_top_spreaders.iterrows():
                            try:
                                posts.add_posts(row.post_id, row.user_id, platform, row.timestamp, row.post_url)
                                reshares.add_reshares(row.post_id, report_id.get('id'), platform, row.num_reshares)
                            except Exception as err:
                                traceback.print_tb(err.__traceback__)
                                logger.error("Error in adding data to post table or reshares table")
                except FileNotFoundError as e:
                    traceback.print_tb(e.__traceback__)
                    logger.error("file {} does not exist".format(file))
        else:
            raise Exception("Already there is a record with file date. Can not proceed!")
            logger.error("There is already records with the file date. Can not proceed!")
    else:
        raise Exception("There is no files related to the that name!")
        logger.error("There is no files related to that name!")

def extract_date_convert_datetime(file_name):
    """
    Extract the date from each file name
    """
    match_str = re.search(r'\d{4}_\d{2}_\d{2}', file_name)
    return datetime.datetime.strptime(match_str.group().replace('_','-'), "%Y-%m-%d")

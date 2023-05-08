"""
Purpose:
    Upload FIB files for top 50 superspreaders to Zenodo.

    Repository: https://doi.org/10.5281/zenodo.7905198
    Zenodo help: https://developers.zenodo.org/

Inputs:
    None

Outputs:
    None

Author: Matthew DeVerna
"""
import glob
import os
import requests
import sys

import pandas as pd

from top_fibers_pkg.utils import get_logger
from top_fibers_pkg.zenodo_helpers import ZenodoAPI

REPO_ROOT = "/home/data/apps/topfibers/repo"
LOG_DIR = "./logs"
LOG_FNAME = "prep_zenodo_files.log"
# ZENODO_DIR = "./data/derived/zenodo_uploads"
ZENODO_DIR = "/Users/mdeverna/temp_data/topfibers"


# For public Zenodo
ACCESS_TOKEN = "see slack pinned messages"
MATCHING_FILE_STR = "fib_indices"
RECORD_ID = 7905198

# For sandbox.zenodo.org (testing playground)
TEST_ACCESS_TOKEN = "see slack pinned messages"
TEST_RECORD_ID = 1199606


if __name__ == "__main__":
    # if not (os.getcwd() == REPO_ROOT):
    #     sys.exit(
    #         "ALL SCRIPTS MUST BE RUN FROM THE REPO ROOT!!\n"
    #         f"\tCurrent directory: {os.getcwd()}\n"
    #         f"\tRepo root        : {REPO_ROOT}\n"
    #     )

    # script_name = os.path.basename(__file__)
    # logger = get_logger(LOG_DIR, LOG_FNAME, script_name=script_name, also_print=True)
    # logger.info("-" * 50)
    # logger.info(f"Begin script: {__file__}")

    zapi = ZenodoAPI(
        TEST_ACCESS_TOKEN,
        TEST_RECORD_ID,
        base_url="https://sandbox.zenodo.org/api/deposit/depositions",
        matching_str=MATCHING_FILE_STR,
    )

    zapi.create_new_version()
    files_to_upload = zapi.get_files_to_upload(ZENODO_DIR, file_suffix="*.csv")
    if len(files_to_upload) == 0:
        print("No files to upload.")
        sys.exit("stopping script")
    zapi.upload_all_files(files_to_upload)
    zapi.publish_changes()

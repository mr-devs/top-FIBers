"""
Purpose:
    Contains functions used to add data to RESHARES table.

Inputs:
    None

Outputs:
    None

Authors: Pasan Kamburugamuwa & Matthew DeVerna
"""
from flask import Flask
from library import backend_util

app = Flask(__name__)

# Add reshares data to table
def add_reshares(post_id, report_id, platform, num_shares):
    """
    Add data to the reshares database table.

    Parameters
    -----------
    - post_id (str): a posts unique id
    - report_id (str): the id for the report that maps to post_id
    - num_shares (int/float): the number of times that post_id was reshared

    Returns
    -----------
    result (dict): {"post_id": post_fetch_id}
    """
    with backend_util.get_db_cursor() as cur:
        try:
            add_reshare = (
                "INSERT INTO reshares "
                "(post_id, report_id, platform, num_reshares) "
                "values (%s, %s, %s, %s) "
                "RETURNING post_id"
            )
            cur.execute(add_reshare, (post_id, report_id, platform, num_shares))
            if cur.rowcount > 0:
                post_fetch_id = cur.fetchone()[0]
                result = {"post_id": post_fetch_id}
            return result
        except Exception as ex:
            raise Exception(ex)


def get_all_reshares():
    """
    Get all data in the reshares table.
    """
    all_reshares = []
    with backend_util.get_db_cursor() as cur:
        select_query = "SELECT post_id, repord_id, platform, num_shares from reshares;"
        cur.execute(select_query)
        if cur.rowcount > 0:
            all_post_details = cur.fetchall()
            for post in all_post_details:
                post_json = {
                    "post_id": post[0],
                    "repord_id": post[1],
                    "platform": post[2],
                    "platform": post[3],
                }
                all_reshares.append(post_json)
    return all_reshares

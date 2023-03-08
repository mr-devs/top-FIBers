"""
Purpose:
    This script used to add the data to fib_indices table
Inputs:
    - The data need to be passed here are,
       |- user_id, report_id, fib_index, total_reshares, username, platform
Outputs:
    The id will be passed.

Authors: Pasan Kamburugamuwa
"""


import logging
from flask import Flask
from library import backend_util

app = Flask(__name__)

#Add fib indices data to database
def add_fib_indices(user_id, report_id, fib_index, total_reshares, username, platform):
    with backend_util.get_db_cursor() as cur:
        try:
            add_fib_index = "INSERT INTO fib_indices (user_id, report_id, fib_index, total_reshares, username, platform) values (%s, %s, %s, %s, %s, %s) RETURNING user_id"
            cur.execute(add_fib_index, (user_id, report_id, fib_index, total_reshares, username, platform))
            if cur.rowcount > 0:
                fib_index_id = cur.fetchone()[0]
                result = {"id" : fib_index_id}
            return result
        except Exception as ex:
            raise Exception(ex)

#Get all the post data
def get_all_posts():
    all_posts = []
    with backend_util.get_db_cursor() as cur:
        select_query = ("SELECT id, post_id, user_id, platform, timestamp, url from fib_indices;")
        cur.execute(select_query)
        if cur.rowcount > 0:
            all_post_details = cur.fetchall()
            for post in all_post_details:
                post_json = {"id": post[0],
                             "post_id" : post[1],
                             "user_id" : post[2],
                             "platform" : post[3],
                             "timestamp" : post[4],
                             "url": post[5]
                             }
                all_posts.append(post_json)
    return all_posts

"""
Purpose:
    This script used to add the data to posts table
Inputs:
    - The data need to be passed here are,
       |- post_id, user_id, platform, timestamp, url
Outputs:
    The post id will be passed.

Authors: Pasan Kamburugamuwa
"""

import logging
from flask import Flask
from library import backend_util

app = Flask(__name__)

#Add post data to database
def add_posts(post_id, user_id, platform, timestamp, url):
    with backend_util.get_db_cursor() as cur:
        try:
            add_post = "INSERT INTO posts (post_id, user_id, platform, timestamp, url) values (%s,%s, %s, %s, %s) RETURNING post_id"
            cur.execute(add_post, (post_id, user_id, platform, timestamp, url))
            if cur.rowcount > 0:
                post_fetch_id = cur.fetchone()[0]
                result = {"post_id" : post_fetch_id}
            return result
        except Exception as ex:
            raise Exception(ex)

#Get all the post data
def get_all_posts():
    all_posts = []
    with backend_util.get_db_cursor() as cur:
        select_query = ("SELECT id, post_id, user_id, platform, timestamp, url from posts;")
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

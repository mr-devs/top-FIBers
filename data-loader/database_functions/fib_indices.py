import logging
from flask import Flask
from library import backend_util
logger = logging.getLogger(__name__)

app = Flask(__name__)

def add_fib_indices(user_id, report_id, fib_index, total_reshares, username, platform):
    logger.info("Add data to fib indices table")
    with backend_util.get_db_cursor() as cur:
        try:
            add_fib_index = "INSERT INTO fib_indices (user_id, report_id, fib_index, total_reshares, username, platform) values (%s, %s, %s, %s, %s, %s) RETURNING user_id"
            cur.execute(add_fib_index, (user_id, report_id, fib_index, total_reshares, username, platform))
            if cur.rowcount > 0:
                fib_index_id = cur.fetchone()[0]
                result = {"id" : fib_index_id}
                logger.info("Successfully added row {} to fib indices table!", fib_index_id)
            else:
                logger.error("There was a a problem in creating the fib indices table!")
            return result
        except Exception as ex:
            print("Error in adding data :", ex)

def get_all_posts():
    logger.info("Get all posts data")
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
                logger.info("Succesfully retrived all posts")
        else:
            logger.info("There is no posts to fetch!")
    return all_posts
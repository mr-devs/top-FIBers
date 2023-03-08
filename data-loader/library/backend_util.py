"""
Purpose:
    This script used to read the data from /home/data/apps/topfibers/repo/data-loader/conf/fibindex.config
    and pass these data to other modules in the data-loader
Inputs:
    - No inputs to this file
Outputs:
    The database configurations will be passed.

Authors: Pasan Kamburugamuwa
"""

import os
import configparser
import logging
import traceback
from psycopg2 import pool
from contextlib import contextmanager

logger = logging.getLogger(__name__)

def get_fib_index_conf():
    try:
        config_file_path = "conf/fibindex.config"
        logger.info('FibIndex conf path : %s', config_file_path)
        config_parser = configparser.ConfigParser()
        config_parser.read(config_file_path)
        return config_parser
    except FileNotFoundError as fnf_error:
        traceback.print_tb(fnf_error.__traceback__)
        raise Exception('Unable to find the fibIndex config file')

def get_flask_host():
    try:
        config = get_fib_index_conf()
        flask_host = config["DEFAULT"]["FlaskHost"]
        return flask_host
    except Exception as exc:
        traceback.print_tb(exc.__traceback__)
        logger.error("Error in finding the fibIndex FlaskHost")
        raise Exception('Unable to find the fibIndex FlaskHost')

def get_flask_port():
    try:
        config = get_fib_index_conf()
        flask_port = config["DEFAULT"]["FlaskPort"]
        return flask_port
    except Exception as exc:
        traceback.print_tb(exc.__traceback__)
        logger.error("Error in finding the fibIndex FlaskPort")
        raise Exception('Unable to find the fibIndex FlaskPort')

def get_flask_debug_mode():
    try:
        config = get_fib_index_conf()
        flask_debug_mode = config["DEFAULT"]["DebugMode"]
        return flask_debug_mode
    except Exception as exc:
        traceback.print_tb(exc.__traceback__)
        logger.error("Error in finding the fibIndex DebugMode")
        raise Exception('Unable to find the fibIndex DebugMode')

def get_database_host():
    try:
        config = get_fib_index_conf()
        database_host = 'localhost'
        return database_host
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logger.error("Error in finding the postgresql database host")
        raise Exception('Unable to find the postgresql database host')

def get_database_port():
    try:
        config = get_fib_index_conf()
        database_port = config["POSTGRESQL_DATABASE"]["database-port"]
        return database_port
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logger.error("Error in finding the postgresql database port")
        raise Exception('Unable to find the postgresql database port')

def get_database_name():
    try:
        config = get_fib_index_conf()
        database_name = config["POSTGRESQL_DATABASE"]["database-name"]
        return database_name
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logger.error("Error in finding the postgresql database name")
        raise Exception('Unable to find the postgresql database name')

def get_database_username():
    try:
        config = get_fib_index_conf()
        database_username = config["POSTGRESQL_DATABASE"]["database-username"]
        return database_username
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logger.error("Error in finding the postgresql database username")
        raise Exception('Unable to find the postgresql database username')

def get_database_password():
    try:
        config = get_fib_index_conf()
        database_password = config["POSTGRESQL_DATABASE"]["database-password"]
        return database_password
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logger.error("Error in finding the postgresql database password")
        raise Exception('Unable to find the postgresql database password')

db = None

try:
    db = pool.SimpleConnectionPool(1,
                                10,
                                host=get_database_host(),
                                database=get_database_name(),
                                user=get_database_username(),
                                password=get_database_password(),
                                port=get_database_port())
except:
    logger.info("Can not connect to FibIndex Database")
    pass


@contextmanager
def get_db_connection():
    con = db.getconn()
    try:
        yield con
    finally:
        db.putconn(con)


@contextmanager
def get_db_cursor():
    with get_db_connection() as connection:
        cursor = connection.cursor()
        try:
            yield cursor
            connection.commit()
        finally:
            cursor.close()

#database.py

import os
import sqlite3
import logging
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row

app_logger = logging.getLogger("app")

class Database():
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
        

    def __init__(self):
        self._pool_flag = False
        try:
            if not self._initialized and os.environ['TEST_ENV'] == "TRUE":
                app_logger.info("Initializing the test sqlite3 database and connection object")
                self.db_connection_object = sqlite3.connect("jaebkatra_test.db")
                self._initialized = True

            elif not self._initialized and os.environ["TEST_ENV"] == "FALSE":
                app_logger.info("intializing the postgres database connection pool object")
                self.db_connection_object = ConnectionPool(os.getenv("POSTGRES_URI"),
                                        kwargs = {'row_factory': dict_row},
                                        min_size=1,
                                        max_size=1,
                                        open=True)
                app_logger.info(f"connection pool initialized successfully")
                self._initialized = True
                self._pool_flag = True
        except Exception as e:
            app_logger.error("failed to initialize or open the database connection object", exc_info=e)
            raise


def yield_pooled_connection():
    db = Database()
    try:
        with db.db_connection_object.connection() as db_conn:
            yield db_conn
    except Exception as e:
        app_logger.error("failed to yield connection object from pool")
        raise
    


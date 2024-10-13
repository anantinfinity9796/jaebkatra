#database.py

import os
import sys
import psycopg
import logging
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row

app_logger = logging.getLogger("app")

class Database():
    _instance = None
    _intialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
        

    def __init__(self):
        try:
            if not self._intialized:
                app_logger.info("intializing the database connection pool object")
                self.pool = ConnectionPool(os.getenv("POSTGRES_URI"),
                                        kwargs = {'row_factory': dict_row},
                                        min_size=1, 
                                        max_size=1,
                                        open=True)
                app_logger.info(f"connection pool initialized successfully")
                self._intialized = True
        except Exception as e:
            app_logger.error("failed to initialize or open the database pool connection object", exc_info=e)
            raise

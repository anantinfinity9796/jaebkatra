#database.py

import os
import sys
import psycopg
from psycopg_pool import ConnectionPool
import logging
from psycopg.rows import dict_row

app_logger = logging.getLogger("app")

class Database():
    def __init__(self, pool=False):
        try:
            app_logger.info("Initializing the POSTGRES database connection")
            if pool:
                self.postgres_connection = ConnectionPool(os.getenv("POSTGRES_URI"),
                                                            row_factory=dict_row,
                                                            min_size=2,
                                                            max_size=3)
            else:
                self.postgres_connection = psycopg.connect(os.getenv("POSTGRES_URI"), row_factory=dict_row)
        except Exception as e:
            app_logger.error("Failed to initialize database connection pool", exc_info=e)
            sys.exit(1)

    def __enter__(self):
        pass

    def __exit__(self):
        pass

    def pool_open(self):
        self.postgres_connection.open()
        return
    
    def pool_close(self):
        self.postgres_connection.close()
        return
    
    def commit(self):
        try:
            self.postgres_connection.commit()
        except Exception as e:
            app_logger.error("failed to commit the operation to the database", exc_info=e)

    def rollback(self,):
        try:
            self.postgres_connection.rollback()
        except Exception as e:
            app_logger.error("failed to rollback the operation to the database", exc_info=e)

    def execute_transaction(self, query_value_list):
        try:
            with self.postgres_connection.connection as conn:
                # cur = conn.cursor()
                with conn.cursor() as cur:
                    with self.postgres_connection.transaction():
                        for query, values in query_value_list:
                            cur.execute(query, values)
                
            # self.postgres_connection.commit()
        except Exception as e:
            app_logger.error("failed to execute transaction rolling back", exc_info=e)
            # self.postgres_connection.rollback()
        # finally:
        #     cur.close()

    def execute_query(self, query, values=None):
        try:
            with self.postgres_connection.connection as conn:
                with conn.cursor() as cur:
                    cur.execute(query, values)
                app_logger.info("query executed successfully")
        except Exception as e:
            app_logger.error(f"Failed to execute query: {query}", exc_info=e)

    def insert_one(self, query, values=None):
        try:
            cur = self.postgres_connection.cursor()
            cur.execute(query, values)
            self.postgres_connection.commit()
            app_logger.info("query executed successfully")
        except Exception as e:
            app_logger.error(f"Failed to execute query: {query}", exc_info=e)
        finally:
            cur.close()
    
    def fetch_one(self, query, values=None):
        try:
            with self.postgres_connection.connection as conn:
                with conn.cursor() as cur:
                    cur.execute(query, values)
                    app_logger.info("query executed successfully")
                    data = cur.fetchone()
            return data
        except Exception as e:
            app_logger.error(f"Failed to execute query: {query}", exc_info=e)
    
    def fetch_all(self, query, values=None):
        try:
            with self.postgres_connection.connection as conn:
                with conn.cursor() as cur:
                    cur.execute(query, values)
                    app_logger.info("query executed successfully")
                    data = cur.fetchall()
            return data
        except Exception as e:
            app_logger.error(f"Failed to execute query: {query}", exc_info=e)

    def delete_one(self, query, values=None):
        try:
            cur = self.postgres_connection.cursor()
            cur.execute(query, values)
            self.postgres_connection.commit()
            app_logger.info("delete query executed successfully")
        except Exception as e:
            app_logger.error(f"Failed to execute delete query: {query}")
        finally:
            cur.close()
        return
        

def get_database_connection():
    conn_object = Database()
    app_logger.info(f"{type(conn_object)}")
    try:
        app_logger.info("Connection initialized")
        yield conn_object
    except Exception as e:
        app_logger.error("Failed to initialize database connection in dependencies", exc_info=e)
        raise
    # finally:
    #     conn_object.close()
    #     app_logger.info("connection closed")
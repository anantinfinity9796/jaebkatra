#database.py

import os
import sys
import psycopg
import logging
from psycopg.rows import dict_row

app_logger = logging.getLogger("app")

class Database():
    def __init__(self):
        try:
            app_logger.info("Initializing the POSTGRES database connection")
            self.postgres_connection = psycopg.connect(os.getenv("POSTGRES_URI"), row_factory=dict_row)
        except Exception as e:
            app_logger.error("Failed to initialize database connection")
            sys.exit(1)

    def __enter__(self):
        pass
    def __exit__(self):
        pass
    def close(self):
        self.postgres_connection.close()
        return
    def execute_transaction(self, query_list, values):
        try:
            cur = self.postgres_connection.cursor()
            with self.postgres_connection.transaction():
                for query in query_list:
                    cur.execute(query, values)
            self.postgres_connection.commit()
        except Exception as e:
            app_logger.error("failed to execute transaction rolling back", exc_info=e)
            self.postgres_connection.rollback()
        finally:
            cur.close()

    def execute_query(self, query):
        try:
            cur = self.postgres_connection.cursor()
            cur.execute(query)
            self.postgres_connection.commit()
            app_logger.info("query executed successfully")
        except Exception as e:
            app_logger.error(f"Failed to execute query: {query}")
        finally:
            cur.close()

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
            cur = self.postgres_connection.cursor()
            cur.execute(query, values)
            self.postgres_connection.commit()
            app_logger.info("query executed successfully")
            return cur.fetchone()
        except Exception as e:
            app_logger.error(f"fetch_one failed for query: {query}", exc_info=e)
            return False
        finally:
            cur.close()
    
    def fetch_all(self, query, values=None):
        try:
            cur = self.postgres_connection.cursor()
            cur.execute(query, values)
            self.postgres_connection.commit()
            app_logger.info("query executed successfully")
            return cur.fetchall()
        except Exception as e:
            app_logger.error(f"fetch_one failed for query: {query}", exc_info=e)
            return False
        finally:
            cur.close()

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
    try:
        app_logger.info("Connection initialized")
        yield conn_object
    except Exception as e:
        app_logger.error("Failed to initialize database connection in dependencies", exc_info=e)
        raise
    finally:
        conn_object.close()
        app_logger.info("connection closed")
#database.py

import os
import psycopg


class Database:

    def __init__(self):
        try:
            # self.connection = psycopg.connect(dbname=os.getenv('POSTGRES_DB'),
            #                               user=os.getenv('POSTGRES_USER'),
            #                               password=os.getenv('POSTGRES_PASSWORD'),
            #                               port=os.getenv('POSTGRES_PORT'),
            #                               host=os.getenv('POSTGRES_HOST'))
            print(os.getenv("POSTGRES_URI"))
            self.postgres_connection = psycopg.connect(os.getenv("POSTGRES_URI"))
        except Exception as e:
            print(e)
            self.postgres_connection = None
    
    def execute_query(self, query):
        try:
            with self.postgres_connection.cursor() as cur:
                print(cur.execute(query))
            self.postgres_connection.commit()
        except Exception as e:
            print(e)
        return 

        
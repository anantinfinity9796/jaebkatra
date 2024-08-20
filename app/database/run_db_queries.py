from db_init_queries import return_db_queries
from database.database import Database

def main():
    queries = return_db_queries()
    db_connection = Database()

    for query in queries:
        print(f"executing_query: {query}")
        db_connection.execute_query(query)

if __name__=='__main__':
    main()
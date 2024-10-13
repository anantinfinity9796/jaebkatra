# transacation_repository.py

import logging
from uuid import UUID

from .repository_interface import Repository
from ..models.transaction import Transaction
from psycopg import Connection

app_logger = logging.getLogger("app")


class TransactionRepository(Repository):

    def __init__(self):
        return
    
    def get_all(self, db_conn:Connection) -> list:
        app_logger.info(f"listing all transactions")
        list_transactions_query = f""" SELECT * FROM transactions;"""
        transactions_list = db_conn.execute(list_transactions_query).fetchall()
        return transactions_list
    
    def get_one(self, db_conn:Connection, transaction_id:UUID) -> dict:
        app_logger.info(f"get transaction details for transaction_id: {transaction_id}")
        get_transaction_query = f""" SELECT * FROM transactions WHERE transaction_id = %(transaction_id)s;"""
        transaction_data = db_conn.execute(get_transaction_query, {"transaction_id":transaction_id}).fetchone()
        return transaction_data
        
    
    def create(self, db_conn:Connection, transaction:Transaction):
        app_logger.info(f"creating a new transaction for user_id: {transaction.user_id}")
        transaction_model_dump = transaction.model_dump()
        insert_transaction_table_query = """
            INSERT INTO transactions (transaction_id, user_id, wallet_id, transaction_amount,
                                            transaction_category, transaction_ts, wallet_type)
                VALUES (%(transaction_id)s, %(user_id)s, %(wallet_id)s, %(transaction_amount)s,
                            %(transaction_category)s, %(transaction_ts)s, %(wallet_type)s);
"""     
        db_conn.execute(insert_transaction_table_query, transaction_model_dump)
        return
        
    
    def delete(self, db_conn:Connection, transaction_id:UUID):
        app_logger.info(f"Deleting transaction with transaction_id: {transaction_id}")
        delete_transaction_query = """DELETE FROM transactions where transaction_id = %(transaction_id)s;"""
        db_conn.execute(delete_transaction_query, {"transaction_id":transaction_id})
        return
        
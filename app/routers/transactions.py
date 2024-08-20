


import logging
from uuid import UUID
from fastapi import APIRouter, status

from ..database.database import Database
from ..models.transaction import Transaction

database_conn = Database()

router = APIRouter(
    prefix="/transactions",
    tags=['transactions']
)




app_logger = logging.getLogger("app")



@router.get("/", status_code=status.HTTP_200_OK)
def list_transactions() -> list:
    try:
        app_logger.info(f"listing all transactions")
        list_transactions_query = f""" SELECT * FROM transactions ;"""
        transactions_list_data = database_conn.fetch_all(query=list_transactions_query)
        return transactions_list_data
    except Exception as e:
        app_logger.error("failed to get transactions list", exc_info=e)


@router.get("/{transaction_id}", status_code=status.HTTP_200_OK)
def get_transaction_details(transaction_id:UUID) -> dict:
    try:
        app_logger.info(f"get transaction details for transaction_id: {transaction_id}")
        get_transaction_query = f""" SELECT * FROM transactions WHERE transaction_id = %s;"""
        transaction_data = database_conn.fetch_one(query=get_transaction_query, values=[transaction_id.hex])
        return transaction_data
    except Exception as e:
        app_logger.error(f"failed to get transaction details for transaction_id: {transaction_id}", exc_info=e)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_transaction(transaction:Transaction):
    try:
        app_logger.info(f"creating a new transaction for user_id: {transaction.user_id}")
        transaction_model_dump = transaction.model_dump()
        app_logger.info(transaction_model_dump)         
        insert_transaction_table_query = """
            INSERT INTO transactions (transaction_id, user_id, wallet_id, transaction_amount,
                                            transaction_category, transaction_ts, wallet_type)
                VALUES (%(transaction_id)s, %(user_id)s, %(wallet_id)s, %(transaction_amount)s,
                            %(transaction_category)s, %(transaction_ts)s, %(wallet_type)s);
"""
        update_wallets_query = """
            UPDATE wallets
            SET consumed_balance = consumed_balance + %(transaction_amount)s
            WHERE wallet_id = %(wallet_id)s;
"""
        database_conn.execute_transaction([insert_transaction_table_query, update_wallets_query], transaction_model_dump)
    except Exception as e:
        app_logger.error(f"failed to create transaction for user_id: {transaction.user_id}", exc_info=e)

# You cannot update a transaction
# @router.patch("/update")
# def modify_user(payload:dict)

# you cannot delete a transaction until and unless a user is deleted
# @router.delete("/{transaction_id}")
# def delete_transaction(transaction_id:UUID):
#     try:
#         app_logger.info(f"Deleting transaction with transaction_id: {transaction_id}")
#         delete_transaction_query = """DELETE FROM transactions where transaction_id = %s;"""
#         database_conn.delete_one(query=delete_transaction_query, values=[transaction_id.hex])
#     except Exception as e:
#         app_logger.error(f"failed to delete transaction: {transaction_id}", exc_info=e)
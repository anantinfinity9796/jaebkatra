# transactions.py


import logging
from uuid import UUID
from typing import Annotated, Any
from fastapi import APIRouter, status, Depends

from ..models.transaction import Transaction
from ..services.transaction_service import TransactionService
from ..database.database import Database, get_database_connection

router = APIRouter(
    prefix="/transactions",
    tags=['transactions']
)




app_logger = logging.getLogger("app")

TransactionsService = Annotated[TransactionService, Depends(TransactionService)]
DbPool =  Annotated[Any, Depends(get_database_connection)]

@router.get("/", status_code=status.HTTP_200_OK)
def list_transactions(db_pool:DbPool, transaction_service: TransactionsService) -> list:
    try:
        transactions_list = transaction_service.list_transactions(db_pool)
        return transactions_list
    except Exception as e:
        app_logger.error("failed to get transactions list", exc_info=e)


@router.get("/{transaction_id}", status_code=status.HTTP_200_OK)
def get_transaction_details(transaction_id:UUID, db_pool:DbPool, transaction_service: TransactionsService) -> dict:
    try:
        transaction_data = transaction_service.get_transaction(db_pool, transaction_id)
        return transaction_data
    except Exception as e:
        app_logger.error(f"failed to get transaction details for transaction_id: {transaction_id}", exc_info=e)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_transaction(transaction:Transaction, db_pool:DbPool, transaction_service: TransactionsService):
    try:
        transaction_service.create_transaction(db_pool, transaction)
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
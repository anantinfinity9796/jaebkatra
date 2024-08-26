# transaction_service.py


from uuid import UUID
from ..models.transaction import Transaction
from ..database.database import Database
from ..repositories.repository_interface import Repository


class TransactionService:

    def list_transactions(self, db_conn:Database, transaction_repo:Repository):
        transactions_list = transaction_repo.get_all(db_conn)
        return transactions_list
    
    def get_transaction(self, db_conn:Database, transaction_repo:Repository, transaction_id:UUID):
        transaction_data = transaction_repo.get_one(db_conn, transaction_id)
        return transaction_data
    
    def create_transaction(self, db_conn:Database, transaction_repo:Repository, transaction:Transaction):
        transaction_repo.create(db_conn, transaction)
        return
    
    def delete_transaction(self, db_conn:Database, transaction_id:UUID, transaction_repo:Repository):
        transaction_repo.delete(db_conn, transaction_id)
        return
# transaction_service.py


from uuid import UUID
from fastapi import Depends
from typing import Annotated


from ..models.transaction import Transaction
from ..database.database import Database
from ..repositories.transaction_repository import TransactionRepository
from ..repositories.budget_repository import BudgetRepository
from ..repositories.wallet_repository import WalletRepository

class TransactionService:

    def __init__(self,
                 transaction_repo: Annotated[TransactionRepository, Depends(TransactionRepository)],
                 budget_repo: Annotated[BudgetRepository, Depends(BudgetRepository)],
                 wallet_repo: Annotated[WalletRepository, Depends(WalletRepository)]):
        
        self.transaction_repo = transaction_repo
        self.budget_repo = budget_repo
        self.wallet_repo = wallet_repo
        return 
        

    def list_transactions(self, db_pool):
        transactions_list = self.transaction_repo.get_all(db_pool)
        return transactions_list
    
    def get_transaction(self, db_pool, transaction_id:UUID):
        transaction_data = self.transaction_repo.get_one(db_pool, transaction_id)
        return transaction_data
    
    def create_transaction(self, db_pool, transaction:Transaction):
        self.transaction_repo.create(db_pool, transaction)
        return
    
    def delete_transaction(self, db_pool, transaction_id:UUID):
        self.transaction_repo.delete(db_pool, transaction_id)
        return
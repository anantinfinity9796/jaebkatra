# budget_service.py


from uuid import UUID
from fastapi import Depends
from typing import Annotated

from ..models.budget import Budget
from ..database.database import Database
from ..repositories.budget_repository import BudgetRepository
from ..repositories.wallet_repository import WalletRepository

class BudgetService:

    def __init__(self,
                 budget_repo: Annotated[BudgetRepository, Depends(BudgetRepository)],
                 wallet_repo: Annotated[WalletRepository, Depends(WalletRepository)]):
        
        self.budget_repo = budget_repo
        self.wallet_repo = wallet_repo
        return 

    def list_budgets(self, db:Database):
        with db.pool.connection() as db_conn:
            budgets_list = self.budget_repo.get_all(db_conn)
        return budgets_list
    
    def get_budget(self, db:Database, budget_id:UUID):
        with db.pool.connection() as db_conn:
            budget_data = self.budget_repo.get_one(db_conn, budget_id)
        return budget_data
    
    def create_budget(self, db:Database, budget:Budget):
        with db.pool.connection() as db_conn:
            self.budget_repo.create(db_conn, budget)
        return
    
    def update_budget(self, db:Database, budget:Budget):
        with db.pool.connection() as db_conn:
            self.budget_repo.update(db_conn, budget)
        return
    
    def update_part_budget(self, db:Database, budget_id:UUID, update_dict:dict):
        with db.pool.connection() as db_conn:
            self.budget_repo.update_part(db_conn, budget_id, update_dict)
        return
    
    def delete_budget(self, db:Database, budget_id:UUID):
        with db.pool.connection() as db_conn:
            self.budget_repo.delete(db_conn, budget_id)
        return
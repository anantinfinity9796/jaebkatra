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

    def list_budgets(self, db_pool):
        budgets_list = self.budget_repo.get_all(db_pool)
        return budgets_list
    
    def get_budget(self, db_pool, budget_id:UUID):
        budget_data = self.budget_repo.get_one(db_pool, budget_id)
        return budget_data
    
    def create_budget(self, db_pool, budget:Budget):
        self.budget_repo.create(db_pool, budget)
        return
    
    def update_budget(self, db_pool, budget:Budget):
        self.budget_repo.update(db_pool, budget)
        return
    
    def update_part_budget(self, db_pool, budget_id:UUID, update_dict:dict):
        self.budget_repo.update_part(db_pool, budget_id, update_dict)
        return
    
    def delete_budget(self, db_pool, budget_id:UUID):
        self.budget_repo.delete(db_pool, budget_id)
        return
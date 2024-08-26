# budget_service.py


from uuid import UUID
from ..models.budget import Budget
from ..database.database import Database
from ..repositories.repository_interface import Repository


class BudgetService:

    def list_budgets(self, db_conn:Database, budget_repo:Repository):
        budgets_list = budget_repo.get_all(db_conn)
        return budgets_list
    
    def get_budget(self, db_conn:Database, budget_repo:Repository, budget_id:UUID):
        budget_data = budget_repo.get_one(db_conn, budget_id)
        return budget_data
    
    def create_budget(self, db_conn:Database, budget_repo:Repository, budget:Budget):
        budget_repo.create(db_conn, budget)
        return
    
    def update_budget(self, db_conn:Database, budget_repo:Repository, budget:Budget):
        budget_repo.update(db_conn, budget)
        return
    
    def update_part_budget(self, db_conn:Database, budget_repo:Repository, budget_id:UUID, update_dict:dict):
        budget_repo.update_part(db_conn, budget_id, update_dict)
        return
    
    def delete_budget(self, db_conn:Database, budget_id:UUID, budget_repo:Repository):
        budget_repo.delete(db_conn, budget_id)
        return
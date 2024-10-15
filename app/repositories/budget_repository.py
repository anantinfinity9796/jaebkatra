# budget_repository.py


import logging
from uuid import UUID

from psycopg import Connection
from .repository_interface import Repository
from ..models.budget import Budget

app_logger = logging.getLogger("app")

class BudgetRepository(Repository):

    def __init__(self):
        return

    def get_all(self, db_conn:Connection) -> list:
        app_logger.info(f"listing all budgets")
        list_budgets_query = """SELECT * FROM budgets;"""
        budgets_list = db_conn.execute(list_budgets_query).fetchall()
        return budgets_list

    def get_one(self, db_conn:Connection, budget_id:UUID) -> dict:
        app_logger.info(f"get budget details for budget_id: {budget_id}")
        get_budget_query = f""" SELECT * FROM budgets WHERE budget_id = %(budget_id)s;"""
        budget_data = db_conn.execute(get_budget_query, {"budget_id":budget_id}).fetchone()
        return budget_data
        
    
    def create(self, db_conn:Connection, budget:Budget):
        budget_model_dump = budget.model_dump()
        create_budget_query = f"""INSERT INTO budgets (budget_id, user_id, wallet_id, created_ts, start_date,
                                                            end_date, budget_amount)
                                    VALUES (%(budget_id)s, %(user_id)s, %(wallet_id)s, %(created_ts)s,
                                                %(start_date)s, %(end_date)s, %(budget_amount)s);"""
        db_conn.execute(create_budget_query, budget_model_dump)
        return
    
    def update(self, db_conn:Connection, budget:Budget):
        app_logger.info(f"updating budget with budget_id: {budget.budget_id}")
        budget_model_dump = budget.model_dump()
        update_budget_query = f"""
            UPDATE budgets
            SET user_id=%(user_id)s,
                wallet_id=%(wallet_id)s,
                start_date=%(start_date)s,
                end_date=%(end_date),
                budget_amount=%(budget_amount)
            WHERE budget_id=%(budget_id)s;
"""
        db_conn.execute(update_budget_query, budget_model_dump)
        return

    def update_part(self):
        raise NotImplementedError
    
    def delete(self, db_conn:Connection, budget_id:UUID):
        app_logger.info(f"Deleting budget with budget_id: {budget_id}")
        delete_budget_query = """DELETE FROM budgets where budget_id = %(budget_id)s;"""
        db_conn.execute(delete_budget_query, {"budget_id":budget_id})
        return
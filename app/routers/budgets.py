# budgets.py


import logging
from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, status, Depends

from ..database.database import Database, get_database_connection
from ..models.budget import Budget
from ..repositories.budget_api_operations import BudgetApiOperations

router = APIRouter(
    prefix="/budgets",
    tags=['budgets']
)


app_logger = logging.getLogger("app")

BudgetApiOperation = Annotated[BudgetApiOperations, Depends(BudgetApiOperations)]
DbConn = Annotated[Database, Depends(get_database_connection)]


@router.get("/", status_code=status.HTTP_200_OK)
def list_budgets(budget_api_operations: BudgetApiOperation, db_conn: DbConn) -> list:
    try:
        list_budgets_query, values = budget_api_operations.get_all()
        budgets_list_data = db_conn.fetch_all(query=list_budgets_query, values=values)
        return budgets_list_data
    except Exception as e:
        app_logger.error("failed to get budgets list", exc_info=e)


@router.get("/{budget_id}", status_code=status.HTTP_200_OK)
def get_budget_details(budget_id:UUID, budget_api_operations: BudgetApiOperation, db_conn: DbConn) -> dict:
    try:
        get_budget_query, values = budget_api_operations.get_one(budget_id)
        budget_data = db_conn.fetch_one(query=get_budget_query, values=values)
        return budget_data
    except Exception as e:
        app_logger.error(f"failed to get budget details for budget_id: {budget_id}", exc_info=e)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_budget(budget:Budget, budget_api_operations: BudgetApiOperation, wallet_api_operations:WalletApiOperation, db_conn: DbConn):
    try:
        app_logger.info(f"creating a new budget for user_id: {budget.user_id}")
        budget_model_dump = budget.model_dump()
        create_budget_query = f"""INSERT INTO budgets (budget_id, user_id, wallet_id, created_ts, start_date,
                                                            end_date, budget_amount)
                                    VALUES (%(budget_id)s, %(user_id)s, %(wallet_id)s, %(created_ts)s,
                                                %(start_date)s, %(end_date)s, %(budget_amount)s);"""
        update_wallet_query  ="""
            UPDATE wallets
            SET allocated_balance = %(budget_amount)s
            WHERE wallet_id = %(wallet_id)s;
"""
        db_conn.execute_transaction([create_budget_query, update_wallet_query], budget_model_dump)
    except Exception as e:
        app_logger.error(f"failed to create budget for user_id: {budget.user_id}", exc_info=e)

# @router.patch("/budgets/update")
# def modify_user(payload:dict)

@router.delete("/{budget_id}", status_code=status.HTTP_200_OK)
def delete_budget(budget_id:UUID, budget_api_operations: BudgetApiOperation, db_conn: DbConn):
    try:
        app_logger.info(f"Deleting budget with budget_id: {budget_id}")
        delete_budget_query = """DELETE FROM budgets where budget_id = %s;"""
        db_conn.delete_one(query=delete_budget_query, values=[budget_id.hex])
    except Exception as e:
        app_logger.error(f"failed to delete budget: {budget_id}", exc_info=e)
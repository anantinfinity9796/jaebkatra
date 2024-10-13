# budgets.py


import logging
from uuid import UUID
from typing import Annotated, Any
from fastapi import APIRouter, status, Depends

from ..database.database import Database
from ..models.budget import Budget
from ..services.budget_service import BudgetService

router = APIRouter(
    prefix="/budgets",
    tags=['budgets']
)


app_logger = logging.getLogger("app")


BudgetsService = Annotated[BudgetService, Depends(BudgetService)]
Db = Annotated[Any, Depends(Database)]


@router.get("/", status_code=status.HTTP_200_OK)
def list_budgets(budget_service: BudgetsService, db:Db) -> list:
    try:
        budgets_list =  budget_service.list_budgets(db)
        return budgets_list
    except Exception as e:
        app_logger.error("failed to get budgets list", exc_info=e)


@router.get("/{budget_id}", status_code=status.HTTP_200_OK)
def get_budget_details(budget_id:UUID, budget_service: BudgetsService, db:Db) -> dict:
    try:
        budget_data = budget_service.get_budget(db, budget_id)
        return budget_data
    except Exception as e:
        app_logger.error(f"failed to get budget details for budget_id: {budget_id}", exc_info=e)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_budget(budget:Budget, budget_service: BudgetsService, db:Db):
    try:
        budget_service.create_budget(db, budget)
    except Exception as e:
        app_logger.error(f"failed to create budget for user_id: {budget.user_id}", exc_info=e)

# @router.patch("/budgets/update")
# def modify_user(payload:dict)

@router.delete("/{budget_id}", status_code=status.HTTP_200_OK)
def delete_budget(budget_id:UUID, budget_service: BudgetsService, db:Db):
    try:
        budget_service.delete_budget(db, budget_id)
    except Exception as e:
        app_logger.error(f"failed to delete budget: {budget_id}", exc_info=e)
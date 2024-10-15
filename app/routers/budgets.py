# budgets.py

import logging
from uuid import UUID
from typing import Annotated, Any
from fastapi import APIRouter, status, Depends, HTTPException

from ..database.database import Database
from ..models.budget import Budget
from ..services.budget_service import BudgetService

app_logger = logging.getLogger("app")

router = APIRouter(
    prefix="/budgets",
    tags=['budgets']
)



BudgetsService = Annotated[BudgetService, Depends(BudgetService)]
Db = Annotated[Database, Depends(Database)]


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Budget])
def list_budgets(budget_service:BudgetsService, db:Db) -> Any:
    try:
        budgets_list =  budget_service.list_budgets(db)
        return budgets_list
    except Exception as e:
        app_logger.error(f"unable to list budgets", exc_info=e)
        raise HTTPException(status_code=500, detail="not able to process the request")


@router.get("/{budget_id}", status_code=status.HTTP_200_OK, response_model=Budget)
def get_budget_details(budget_id:UUID, budget_service: BudgetsService, db:Db) -> Any:
    try:
        budget_data = budget_service.get_budget(db, budget_id)
        if budget_data is None:
            raise HTTPException(status_code=404, detail=f"budget with budget_id: {budget_id} not found")
        return budget_data
    except Exception as e:
        app_logger.error(f"failed to get budget details for budget_id: {budget_id}", exc_info=e)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_budget(budget:Budget, budget_service: BudgetsService, db:Db):
    try:
        budget_service.create_budget(db, budget)
        app_logger.info(f"budget with budget_id: {budget.budget_id} in wallet: {budget.wallet_id} for user: {budget.user_id} has been created")
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
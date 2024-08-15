# budget.py


from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel


class Budget(BaseModel):
    budget_id: UUID
    user_id: UUID
    wallet_id: UUID
    created_ts: datetime
    start_date: date
    end_date: date
    budget_amount: float = 0.0
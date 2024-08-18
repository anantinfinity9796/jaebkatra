# budget.py

import uuid
from uuid import UUID
from dataclasses import dataclass
from datetime import datetime, date, timedelta
from pydantic import BaseModel, Field

@dataclass
class Budget(BaseModel):

    budget_id: UUID = Field(default_factory=lambda: uuid.uuid4().hex)
    user_id: UUID
    wallet_id: UUID
    created_ts: datetime = Field(default_factory=lambda:  datetime.now())
    start_date: date = Field(default_factory=lambda : datetime.now().date())
    end_date: date
    budget_amount: float
# budget.py

import uuid
from uuid import UUID
from dataclasses import dataclass
from datetime import datetime, date, timedelta
from pydantic import BaseModel, Field


class Budget(BaseModel):
    budget_id: UUID = Field(default_factory=uuid.uuid4)
    user_id: UUID
    wallet_id: UUID
    created_ts: datetime = Field(default_factory=datetime.now)
    start_date: date = Field(default_factory=datetime.now().date)
    end_date: date
    budget_amount: float
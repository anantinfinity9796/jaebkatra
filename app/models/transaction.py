# transaction.py

import uuid
from uuid import UUID
from dataclasses import dataclass
from datetime import datetime
from pydantic import BaseModel, Field

@dataclass
class Transaction(BaseModel):
    transaction_id: UUID = Field(default_factory=lambda: uuid.uuid4().hex)
    user_id: UUID
    wallet_id: UUID
    transaction_amount: float
    transaction_category: str
    transaction_ts: datetime = Field(default_factory=lambda: datetime.now())
    wallet_type: str = None
    
    
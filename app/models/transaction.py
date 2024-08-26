# transaction.py

import uuid
from uuid import UUID
from dataclasses import dataclass
from datetime import datetime
from pydantic import BaseModel, Field

@dataclass
class Transaction(BaseModel):
    transaction_id: UUID = Field(default_factory=uuid.uuid4)
    user_id: UUID
    wallet_id: UUID
    transaction_amount: float
    transaction_category: str
    transaction_ts: datetime = Field(default_factory=datetime.now)
    wallet_type: str = None
    
    
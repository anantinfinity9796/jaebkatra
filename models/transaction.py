# transaction.py

from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class Transaction(BaseModel):
    transaction_id: UUID
    user_id: UUID
    wallet_id: UUID
    transaction_amount: float = 0.0
    transaction_category: str
    transaction_ts: datetime
    wallet_type: str | None = None
    
    
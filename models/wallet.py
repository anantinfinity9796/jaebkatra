# wallet.py

from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class Wallet(BaseModel):

    wallet_id: UUID
    user_id: UUID
    name: str
    created_ts: datetime
    allocated_balance: float = 0.0
    consumed_balance: float = 0.0
    remaining_balance: float = 0.0
    wallet_type: str
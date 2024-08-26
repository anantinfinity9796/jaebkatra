# wallet.py

import uuid
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

@dataclass
class Wallet(BaseModel):

    wallet_id: UUID = Field(default_factory=uuid.uuid4)
    user_id: UUID
    name: str
    created_ts: datetime  = Field(default_factory=datetime.now)
    allocated_balance: float
    consumed_balance: float = 0.00
    wallet_type: str
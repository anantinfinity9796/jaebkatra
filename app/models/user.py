# user.py

import uuid
from uuid import UUID
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from datetime import datetime
from dataclasses import dataclass


# @dataclass
class User(BaseModel):

    user_id : UUID = Field(default_factory=uuid.uuid4)
    name: str
    created_ts: datetime = Field(default_factory=datetime.now)
    phone: str = None
    wallets: list[UUID] = []
    family_members: list[UUID] = []

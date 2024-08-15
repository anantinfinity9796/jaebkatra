# user.py

from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):

    user_id : UUID
    name: str
    created_ts: datetime
    phone: str | None = None
    wallets: list[UUID] | None = None
    family_members: list[UUID] | None = None

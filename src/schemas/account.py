from datetime import datetime

from pydantic import BaseModel, PositiveFloat


class AccountIn(BaseModel):
    balance: PositiveFloat


class AccountOut(BaseModel):
    user_id: int
    balance: PositiveFloat
    created_at: datetime

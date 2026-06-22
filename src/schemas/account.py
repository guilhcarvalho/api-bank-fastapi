from datetime import datetime

from pydantic import BaseModel, ConfigDict, PositiveFloat


class Message(BaseModel):
    message: str


class AccountIn(BaseModel):
    balance: PositiveFloat


class AccountOut(BaseModel):
    id: int
    balance: PositiveFloat
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class AccountList(BaseModel):
    accounts: list[AccountOut]

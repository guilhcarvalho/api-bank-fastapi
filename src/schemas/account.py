from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class AccountIn(BaseModel):
    user: str
    email: EmailStr
    password: str


class AccountOut(BaseModel):
    user: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class AccountList(BaseModel):
    accounts: list[AccountOut]

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, PositiveFloat


class TransactionType(Enum):
    DEPOSIT = 'deposit'
    WITHDRAWAL = 'withdrawal'


class TransactionIn(BaseModel):
    account_user: str
    type: TransactionType
    amount: PositiveFloat
    currency: str

    class Config:
        use_enum_values = True


class TransactionOut(BaseModel):
    transaction_number: int
    account_user: str
    type: TransactionType
    amount: PositiveFloat
    currency: str
    timestamp: datetime

    class Config:
        from_attributes = True


class TransactionsList(BaseModel):
    transactions: list[TransactionOut]

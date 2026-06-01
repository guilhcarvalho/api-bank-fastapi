from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class TransactionType(Enum):
    DEPOSIT = 'deposit'
    WITHDRAWAL = 'withdrawal'


class TransactionIn(BaseModel):
    account: int
    type: TransactionType
    amount: int
    currency: str
    timestamp: datetime

    class Config:
        use_enum_values = True

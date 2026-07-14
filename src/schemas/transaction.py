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
    timestamp: datetime

    class Config:
        use_enum_values = True

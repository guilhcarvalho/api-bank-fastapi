from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import table_registry
from src.schemas.transaction import TransactionType

if TYPE_CHECKING:
    from src.models.account import Account


@table_registry.mapped_as_dataclass
class Transaction:
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    account_user: Mapped[str] = mapped_column(ForeignKey('accounts.user'))
    type: Mapped[TransactionType] = mapped_column(
        SQLEnum(
            TransactionType, values_callable=lambda e: [i.value for i in e]
        )
    )
    amount: Mapped[float] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    account: Mapped['Account'] = relationship(
        back_populates='transactions', init=False
    )

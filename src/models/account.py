from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import table_registry

if TYPE_CHECKING:
    from src.models.transaction import Transaction


@table_registry.mapped_as_dataclass
class Account:
    __tablename__ = 'accounts'
    __table_args__ = (
        UniqueConstraint('user', name='uq_accounts_user'),
        UniqueConstraint('email', name='uq_accounts_email'),
    )

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    transactions: Mapped[list['Transaction']] = relationship(
        back_populates='account', init=False, default_factory=list
    )

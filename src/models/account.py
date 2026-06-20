from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column

from src.database import table_registry


@mapped_as_dataclass(table_registry)
class Account:
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    balance: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

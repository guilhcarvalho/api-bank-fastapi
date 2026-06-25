from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.account import Account


@pytest.mark.asyncio
async def test_create_account(session: AsyncSession, mock_db_time):
    with mock_db_time(model=Account) as time:
        USER, EMAIL, PASSWORD = 'test', 'test@api-bank.com', 'password'

        new_account = Account(
            user=USER,
            email=EMAIL,
            password=PASSWORD,
        )
        session.add(new_account)
        await session.commit()

        account = await session.scalar(
            select(Account).where(
                Account.user == USER,
                Account.email == EMAIL,
                Account.password == PASSWORD,
            )
        )
        assert asdict(account) == {
            'id': 1,
            'user': USER,
            'email': EMAIL,
            'password': PASSWORD,
            'created_at': time,
            'updated_at': time,
        }

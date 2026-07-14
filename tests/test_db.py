from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.account import Account
from src.models.transaction import Transaction
from tests.conftest import TransactionFactory


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
            'transactions': [],
        }


@pytest.mark.asyncio
async def test_create_transaction(
    session: AsyncSession, mock_db_time, account
):
    with mock_db_time(model=Transaction) as time:
        new_transaction = TransactionFactory(account_user=account.user)
        session.add(new_transaction)
        await session.commit()
        transaction = await session.scalar(
            select(Transaction).where(
                Transaction.account_user == account.user,
                Transaction.type == new_transaction.type,
            )
        )
        assert transaction.id == 1
        assert transaction.account_user == account.user
        assert transaction.type == new_transaction.type
        assert transaction.amount == new_transaction.amount
        assert transaction.currency == new_transaction.currency
        assert transaction.timestamp == time

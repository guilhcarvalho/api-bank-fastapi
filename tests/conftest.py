from contextlib import contextmanager
from datetime import datetime

import factory
import pytest
import pytest_asyncio
from factory import fuzzy
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

import src.models  # noqa: F401
from src.database import get_session, table_registry
from src.main import app
from src.models.account import Account
from src.models.transaction import Transaction, TransactionType
from src.security import get_password_hash


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def account(session: AsyncSession):
    password = 'supersecrettest'
    account = UserFactory(password=get_password_hash(password))
    session.add(account)
    await session.commit()
    await session.refresh(account)
    account.clean_password = password

    return account


@pytest_asyncio.fixture
async def transaction(session: AsyncSession, account):
    transaction = TransactionFactory(account_user=account.user)
    session.add(transaction)
    await session.commit()
    await session.refresh(transaction)

    return transaction


@pytest_asyncio.fixture
async def other_account(session: AsyncSession):
    password = 'supersecrettest'
    account = UserFactory(password=get_password_hash(password))
    session.add(account)
    await session.commit()
    await session.refresh(account)
    account.clean_password = password

    return account


@contextmanager
def _mock_db_time(*, model, time=datetime(2026, 1, 1)):

    def fake_time_hook(mapper, connection, target):
        if isinstance(target, model):
            for field in ('created_at', 'updated_at', 'timestamp'):
                if hasattr(target, field):
                    setattr(target, field, time)

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def token(client, account):
    response = client.post(
        '/auth/',
        data={'username': account.email, 'password': account.clean_password},
    )
    return response.json()['access_token']


class UserFactory(factory.Factory):
    class Meta:
        model = Account

    user = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.user}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.user}@example.com')


class TransactionFactory(factory.Factory):
    class Meta:
        model = Transaction

    account_user = factory.Sequence(lambda n: f'test{n}')
    type = fuzzy.FuzzyChoice(TransactionType)
    amount = fuzzy.FuzzyFloat(0.0, 1000.0)
    currency = 'BRL'

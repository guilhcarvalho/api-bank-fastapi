from contextlib import asynccontextmanager
from datetime import UTC, datetime
from http import HTTPStatus

from fastapi import FastAPI

import src.models  # noqa: F401
from src.controllers import account
from src.database import engine, table_registry
from src.schemas.transaction import TransactionIn


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan, title='Bank API FastAPI')


app.include_router(account.router, tags=['account'])


@app.get(
    '/transaction/', status_code=HTTPStatus.OK, response_model=TransactionIn
)
async def read_saque():
    return {
        'account': 1,
        'type': 'deposit',
        'amount': 150,
        'currency': 'BRL',
        'timestamp': datetime.now(UTC),
    }

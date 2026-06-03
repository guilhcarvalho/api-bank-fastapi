from contextlib import asynccontextmanager
from datetime import UTC, datetime
from http import HTTPStatus

from fastapi import FastAPI

import src.models  # noqa: F401
from src.controllers import account
from src.database import database, engine, metadata
from src.schemas.transaction import TransactionIn


@asynccontextmanager
async def lifespan(app: FastAPI):
    metadata.create_all(engine)
    await database.connect()
    yield
    await database.disconnect()


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

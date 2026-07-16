from contextlib import asynccontextmanager

from fastapi import FastAPI

import src.models  # noqa: F401
from src.controllers import account, auth, transaction
from src.database import engine, table_registry


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan, title='Bank API FastAPI')


app.include_router(account.router, tags=['account'])
app.include_router(auth.router, tags=['auth'])
app.include_router(transaction.router, tags=['transaction'])

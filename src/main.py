import asyncio
import sys

from fastapi import FastAPI

import src.models  # noqa: F401
from src.controllers import account, auth, transaction

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI(title='Bank API FastAPI')

app.include_router(account.router, tags=['account'])
app.include_router(auth.router, tags=['auth'])
app.include_router(transaction.router, tags=['transaction'])

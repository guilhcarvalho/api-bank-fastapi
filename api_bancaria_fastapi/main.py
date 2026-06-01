from datetime import UTC, datetime
from http import HTTPStatus

from fastapi import FastAPI

from .schemas import TransactionIn

app = FastAPI(title='Bank API FastAPI')


@app.get('/transaction/', status_code=HTTPStatus.OK, response_model=TransactionIn)
async def read_saque():
    return {
        'account': 1,
        'type': 'deposit',
        'amount': 150,
        'currency': "BRL",
        'timestamp': datetime.now(UTC)
        }

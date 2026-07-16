from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session
from src.models.account import Account
from src.models.transaction import Transaction
from src.schemas.transaction import (
    TransactionIn,
    TransactionOut,
    TransactionsList,
)
from src.security import get_current_user

router = APIRouter(prefix='/transactions')


# Create
@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=TransactionOut,
)
async def create_transaction(
    post: TransactionIn,
    session: Session = Depends(get_session),
    current_user: Account = Depends(get_current_user),
):
    if current_user.user != post.account_user:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions',
        )

    db_transaction = Transaction(
        account_user=post.account_user,
        type=post.type,
        amount=post.amount,
        currency=post.currency,
    )

    session.add(db_transaction)
    await session.commit()
    await session.refresh(db_transaction)
    return db_transaction


# Read
@router.get(
    '/{transaction_number}',
    status_code=HTTPStatus.OK,
    response_model=TransactionOut,
)
async def read_transaction(
    transaction_number: int,
    session: Session = Depends(get_session),
):
    query = await session.scalar(
        select(Transaction).where(
            Transaction.transaction_number == transaction_number
        )
    )
    return query


# Read all per user
@router.get(
    '/bank_statement/{account_user}',
    status_code=HTTPStatus.OK,
    response_model=TransactionsList,
)
async def read_user_transactions(
    account_user: str,
    session: Session = Depends(get_session),
    current_user: Account = Depends(get_current_user),
):
    if current_user.user != account_user:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions',
        )
    query = await session.scalars(select(Transaction))
    return {'transactions': query.all()}

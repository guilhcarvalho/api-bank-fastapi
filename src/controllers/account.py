from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.database import get_session
from src.models.account import Account
from src.schemas.account import AccountIn, AccountList, AccountOut

router = APIRouter(prefix='/accounts')


# Read users
@router.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=AccountList,
)
async def read_accounts(
    session: Session = Depends(get_session),
):
    query = await session.scalars(select(Account))
    return {'accounts': query.all()}


# Read user
@router.get(
    '/user',
    status_code=HTTPStatus.OK,
    response_model=AccountOut,
)
async def read_account(session: Session = Depends(get_session)):
    query = await session.scalar(select(Account))
    return query


# Create users
@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=AccountOut,
)
async def create_account(
    post: AccountIn,
    session: Session = Depends(get_session),
):
    db_account = await session.scalar(
        select(Account).where(
            (Account.user == post.user) | (Account.email == post.email)
        )
    )
    if db_account:
        if db_account.user == post.user:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='User already exists'
            )
        elif db_account.email == post.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Email already exists.'
            )
    db_account = Account(
        user=post.user, email=post.email, password=post.password
    )

    session.add(db_account)
    await session.commit()
    await session.refresh(db_account)
    return db_account


# Update users
@router.put(
    '/{account_user}',
    status_code=HTTPStatus.OK,
    response_model=AccountOut,
)
async def update_account(
    account_user: str,
    put: AccountIn,
    session: Session = Depends(get_session),
):
    db_account = await session.scalar(
        select(Account).where(Account.user == account_user)
    )
    if not db_account:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Account not found'
        )
    db_account.user = put.user
    db_account.password = put.password
    db_account.email = put.email
    try:
        await session.commit()
        await session.refresh(db_account)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='User or Email already exists',
        )
    return db_account


# Delete users
@router.delete(
    '/{account_user}',
    status_code=HTTPStatus.OK,
)
async def delete_account(
    account_user: str, session: Session = Depends(get_session)
):
    db_account = await session.scalar(
        select(Account).where(Account.user == account_user)
    )
    if not db_account:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Account not found'
        )
    session.delete(db_account)
    await session.commit()
    return {'message': 'Account deleted'}

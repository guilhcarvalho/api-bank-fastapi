from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session
from src.models.account import Account
from src.schemas.account import AccountIn, AccountList, AccountOut, Message

router = APIRouter(prefix='/accounts')


# Read users
@router.get(
    '/get-accounts/',
    status_code=HTTPStatus.OK,
    response_model=list[AccountOut],
)
async def read_account():
    query = Account.select()
    return await get_session.fetch_all(query)


# Create users
@router.post(
    '/post-accounts/',
    status_code=HTTPStatus.CREATED,
    response_model=AccountOut,
)
async def create_account(post: AccountIn):
    now = datetime.now()
    command = Account.insert().values(balance=post.balance, created_at=now)
    last_id = await get_session.execute(command)
    return {
        **post.model_dump(),
        'user_id': last_id,
        'balance': post.balance,
        'created_at': now,
    }


# Update users
@router.put(
    '/put-accounts/{account_id}',
    status_code=HTTPStatus.OK,
    response_model=AccountOut,
)
async def update_account(account_id: int, put: AccountIn):
    select_command = select(Account).where(Account.c.user_id == account_id)
    data_exist = await get_session.fetch_one(select_command)

    if not data_exist:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not Found!'
        )
    update_command = (
        Account
        .update()
        .values(
            balance=put.balance,
        )
        .where(Account.c.user_id == account_id)
    )
    await get_session.execute(update_command)
    return {
        **put.model_dump(),
        'user_id': account_id,
        'balance': put.balance,
        'created_at': datetime.now(),
    }


# Delete users
@router.delete(
    '/delete-users/{account_id}',
    status_code=HTTPStatus.OK,
)
async def delete_account(account_id: int):
    select_command = select(Account).where(Account.c.user_id == account_id)
    data_exist = await get_session.fetch_one(select_command)

    if not data_exist:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not Found!'
        )

    delete_command = Account.delete().where(Account.c.user_id == account_id)
    await get_session.execute(delete_command)
    return {'message': f'User {account_id} deleted successfully!'}


##############################################################################
# APENAS UNS TESTES E TESTES E TESTES ########################
@router.post(
    '/tests/', status_code=HTTPStatus.CREATED, response_model=AccountOut
)
def create_post_test(
    account: AccountIn, session: Session = Depends(get_session)
):
    db_user = session.scalar(
        select(Account).where((Account.balance == account.balance))
    )
    if db_user:
        if db_user.balance < 0:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail='Balance smaller than 0',
            )
    db_user = Account(
        balance=account.balance,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get('/tests/', response_model=AccountList)
def read_test(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    tests = session.scalars(select(Account).offset(skip).limit(limit)).all()
    return {'accounts': tests}


@router.put('/{id}/', response_model=AccountOut)
def update_test(
    id: int, account: AccountIn, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(Account).where(Account.id == id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Account not found'
        )

    db_user.balance = account.balance
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete('/{id}/', response_model=Message)
def delete_test(id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(Account).where(Account.id == id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Account not found'
        )
    session.delete(db_user)
    session.commit()
    return {'message': 'Account deleted'}

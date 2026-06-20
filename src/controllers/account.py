from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from src.database import get_session
from src.models.account import Account
from src.schemas.account import AccountIn, AccountOut

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

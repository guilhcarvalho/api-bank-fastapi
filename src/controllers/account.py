from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter

from src.database import database
from src.models.account import accounts
from src.schemas.account import AccountIn, AccountOut

router = APIRouter(prefix='/accounts')


# Read users
@router.get(
    '/get-accounts/',
    status_code=HTTPStatus.OK,
    response_model=list[AccountOut],
)
async def read_account():
    query = accounts.select()
    return await database.fetch_all(query)


# Create users
@router.post(
    '/post-accounts/',
    status_code=HTTPStatus.CREATED,
    response_model=AccountOut,
)
async def create_account(post: AccountIn):
    now = datetime.now()
    command = accounts.insert().values(
        balance=post.balance, 
        created_at=now
    )
    last_id = await database.execute(command)
    return {**post.model_dump(),
            'user_id': last_id,
            'balance': post.balance,
            'created_at': datetime.now()
    }


# Update users
@router.put(
    '/put-accounts/{account_id}',
    status_code=HTTPStatus.OK,
    response_model=AccountOut,
)
async def update_account(account_id: int, put: AccountOut):
    command = (
        accounts
        .update()
        .values(
            balance=put.balance,
        )
        .where(accounts.c.id == account_id)
    )
    await database.execute(command)
    return {**put.model_dump(), 'user_id': account_id}


# Delete users
@router.delete(
    '/delete-users/{account_id}',
    status_code=HTTPStatus.OK,
)
async def delete_account(account_id: int):
    command = (
        accounts.delete().where(accounts.c.user_id == account_id)
    )
    await database.execute(command)
    return account_id
     
from dataclasses import asdict

from sqlalchemy import select

from src.models.account import Account


def test_create_user(session, mock_db_time):
    with mock_db_time(model=Account) as time:
        BALANCE = 10.1

        new_account = Account(balance=BALANCE)
        session.add(new_account)
        session.commit()

        account = session.scalar(
            select(Account).where(Account.balance == BALANCE)
        )
        assert asdict(account) == {
            'id': 1,
            'balance': BALANCE,
            'created_at': time,
        }

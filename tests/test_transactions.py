from http import HTTPStatus

from src.schemas.transaction import TransactionOut
from tests.conftest import TransactionFactory


def test_create_transaction(client, account, token):
    new_transaction = TransactionFactory(account_user=account.user)
    response = client.post(
        '/transactions/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'account_user': account.user,
            'type': new_transaction.type.value,
            'amount': new_transaction.amount,
            'currency': new_transaction.currency,
        },
    )
    print(response.json())
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'transaction_number': response.json()['transaction_number'],
        'account_user': account.user,
        'type': new_transaction.type.value,
        'amount': new_transaction.amount,
        'currency': new_transaction.currency,
        'timestamp': response.json()['timestamp'],
    }


def test_read_transaction(client, transaction):
    transaction_schema = TransactionOut.model_validate(transaction).model_dump(
        mode='json'
    )
    response = client.get(f'/transactions/{transaction.transaction_number}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == transaction_schema


def test_read_user_transaction(client, transaction, token):
    transaction_schema = TransactionOut.model_validate(transaction).model_dump(
        mode='json'
    )
    response = client.get(
        f'/transactions/bank_statement/{transaction.account_user}',
        headers={'Authorization': f'Bearer {token}'},
    )
    print(response.json())
    assert response.json() == {'transactions': [transaction_schema]}

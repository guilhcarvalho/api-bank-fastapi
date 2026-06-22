from http import HTTPStatus

from src.schemas.account import AccountOut


def test_create_post(client):
    response = client.post('/accounts/tests/', json={'balance': 1000})
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'balance': 1000,
        'id': 1,
        'created_at': response.json()['created_at'],
        'updated_at': response.json()['updated_at'],
    }


def test_read_tests(client):
    response = client.get('/accounts/tests/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'accounts': []}


def test_read_accounts_with_fixture(client, account):
    account_schema = AccountOut.model_validate(account).model_dump(mode='json')
    response = client.get('/accounts/tests/')
    assert response.json() == {'accounts': [account_schema]}


def test_update_test(client, account):
    response = client.put(
        '/accounts/1/',
        json={
            'balance': 150,
        },
    )

    expected = (
        AccountOut
        .model_validate(account)
        .model_copy(update={'balance': 150})
        .model_dump(mode='json')
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected


def test_delete_test(client, account):
    response = client.delete('/accounts/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Account deleted'}

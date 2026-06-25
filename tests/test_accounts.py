from http import HTTPStatus

from src.schemas.account import AccountOut


def test_create_account(client):
    response = client.post(
        '/accounts/',
        json={
            'user': 'test',
            'email': 'test@api-banktest.com',
            'password': 'supersecrettest',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'user': 'test',
        'email': 'test@api-banktest.com',
        'password': 'supersecrettest',
        'created_at': response.json()['created_at'],
        'updated_at': response.json()['updated_at'],
    }


def test_read_accounts(client):
    response = client.get('/accounts/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'accounts': []}


def test_read_accounts_with_fixture(client, account):
    account_schema = AccountOut.model_validate(account).model_dump(mode='json')
    response = client.get('/accounts/')
    assert response.json() == {'accounts': [account_schema]}


def test_update_user(client, account):
    response = client.put(
        f'/accounts/{account.user}',
        json={
            'user': 'testUpdate',
            'email': 'testUpdate@api-banktest.com',
            'password': 'supersecrettest',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'user': 'testUpdate',
        'email': 'testUpdate@api-banktest.com',
        'password': 'supersecrettest',
        'created_at': response.json()['created_at'],
        'updated_at': response.json()['updated_at'],
    }


def test_integrity_error(client, account):
    client.post(
        '/accounts/',
        json={
            'user': 'testIntegrity',
            'email': 'testIntegrity@api-banktest.com',
            'password': 'supersecrettest',
        },
    )
    response_update = client.put(
        f'/accounts/{account.user}',
        json={
            'user': 'testIntegrity',
            'email': 'testIntegrity@api-banktest.com',
            'password': 'supersecrettest',
        },
    )
    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {'detail': 'User or Email already exists'}


def test_delete_test(client, account):
    response = client.delete(f'/accounts/{account.user}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Account deleted'}

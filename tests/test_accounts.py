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


def test_update_user(client, account, token):
    response = client.put(
        f'/accounts/{account.user}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'user': account.user,
            'email': 'testUpdate@api-banktest.com',
            'password': 'supersecrettest',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'user': account.user,
        'email': 'testUpdate@api-banktest.com',
        'created_at': response.json()['created_at'],
        'updated_at': response.json()['updated_at'],
    }


def test_update_integrity_error(client, account, other_account, token):
    response_update = client.put(
        f'/accounts/{account.user}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'user': other_account.user,
            'email': 'testIntegrity@api-banktest.com',
            'password': 'supersecrettest',
        },
    )
    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {'detail': 'User or Email already exists'}


def test_delete_account(client, account, token):
    response = client.delete(
        f'/accounts/{account.user}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Account deleted'}


def test_update_account_with_wrong_account(client, other_account, token):
    response = client.put(
        f'/accounts/{other_account.user + "usertest"}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'user': 'Joao',
            'email': 'testUpdate@api-banktest.com',
            'password': 'supersecrettest',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_account_wrong_acount(client, other_account, token):
    response = client.delete(
        f'/accounts/{other_account.user}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}

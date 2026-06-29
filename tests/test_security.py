from http import HTTPStatus

from jwt import decode

from src.security import create_access_token
from src.settings import Settings


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)
    decoded = decode(
        token,
        Settings().SECRET_KEY,
        Settings().ALGORITHM,
    )
    assert decoded['test'] == data['test']
    assert 'exp' in decoded


def test_jwt_invalid_token(client):
    response = client.delete(
        '/accounts/userExample',
        headers={'Authorization': 'Bearer token-invalido'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_not(client):
    data = {'no-email': 'test'}
    token = create_access_token(data)

    response = client.delete(
        '/accounts/userExample',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_does_not_exists(client):
    data = {'sub': 'test@test'}
    token = create_access_token(data)

    response = client.delete(
        '/accounts/userExample',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}

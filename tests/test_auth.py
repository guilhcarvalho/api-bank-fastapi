from http import HTTPStatus

from freezegun import freeze_time


def test_get_token(client, account):
    response = client.post(
        '/auth/',
        data={
            'username': account.email,
            'password': account.clean_password,
        },
    )
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_token_expired_after_time(client, account):
    with freeze_time('2026-07-08 12:00:00'):
        response = client.post(
            '/auth/',
            data={
                'username': account.email,
                'password': account.clean_password,
            },
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2026-07-08 12:31:00'):
        response = client.put(
            f'/accounts/{account.user}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'wrongwrong',
                'email': 'wrong@wrong.com',
                'password': 'wrong123',
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_token_inexistent_account(client):
    response = client.post(
        '/auth/',
        data={'username': 'no_user@no_domain.com', 'password': 'test123'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_token_wrong_password(client, account):
    response = client.post(
        '/auth/', data={'username': account.email, 'password': 'wrongpassword'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_refresh_token(client, account, token):
    response = client.post(
        '/auth/refresh',
        headers={'Authorization': f'Bearer {token}'},
    )
    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'bearer'


def test_token_expired_dont_refresh(client, account):
    with freeze_time('2026-07-08 12:00:00'):
        response = client.post(
            '/auth/',
            data={
                'username': account.email,
                'password': account.clean_password,
            },
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

        with freeze_time('2026-07-08 12:31:00'):
            response = client.post(
                '/auth/refresh',
                headers={'Authorization': f'Bearer {token}'},
            )

            assert response.status_code == HTTPStatus.UNAUTHORIZED
            assert response.json() == {
                'detail': 'Could not validate credentials'
            }

import json

import pytest
from model_bakery import baker


@pytest.fixture
def google_token(faker):
    return faker.uuid4()


@pytest.fixture
def user_email(faker):
    return faker.email()


@pytest.fixture
def requests_get(mocker):
    return mocker.patch('requests.get')


@pytest.fixture
def success_response(requests_get, user_email):
    requests_get.return_value.text = json.dumps({'email': user_email})


@pytest.fixture
def user_allowed(user_email):
    return baker.make('UserAllowed', email=user_email)


@pytest.fixture
def user_allowed_not_registered(user_email):
    return baker.make('UserAllowed', email=user_email)


@pytest.fixture
def user(user_allowed):
    return baker.make('User', email=user_allowed.email)


@pytest.fixture
def token_data(faker):
    return {
        'refresh_token': faker.uuid4(),
        'access_token': faker.uuid4(),
    }


@pytest.fixture
def mocker_refresh_token(mocker):
    return mocker.patch('lavocat.api.v1.core.facade.RefreshToken.for_user')


@pytest.fixture
def refreshed_token(mocker_refresh_token, token_data):
    class Token:
        def __str__(self):
            return token_data['refresh_token']

        @property
        def access_token(self):
            return token_data['access_token']

    mocker_refresh_token.return_value = Token()


@pytest.fixture
def mocker_authenticate(mocker):
    return mocker.patch('lavocat.api.v1.core.facade.authenticate')

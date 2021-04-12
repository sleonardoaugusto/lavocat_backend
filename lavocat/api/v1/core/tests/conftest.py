import pytest


@pytest.fixture
def google_token(faker):
    return faker.uuid4()


@pytest.fixture
def google_auth_mock(mocker):
    return mocker.patch('lavocat.api.v1.core.facade.google_auth', return_value={})


@pytest.fixture
def user_email(faker):
    return faker.email()


@pytest.fixture
def token_data(faker):
    return {
        'refresh_token': faker.uuid4(),
        'access_token': faker.uuid4(),
    }

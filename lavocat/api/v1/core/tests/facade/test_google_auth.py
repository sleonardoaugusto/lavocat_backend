import pytest
from rest_framework import status

from lavocat.api.v1.core import facade
from lavocat.api.v1.core.facade import GOOGLE_AUTH_URL, Unauthorized, UserNotAllowed


def test_must_call_get_with_params(
    google_token, requests_get, success_response, user_allowed, authenticate_mocked
):
    requests_get.return_value.text = success_response
    facade.google_auth(google_token)
    requests_get.assert_called_once_with(
        GOOGLE_AUTH_URL, params={'access_token': google_token}
    )


def test_google_auth_unauthorized(google_token, requests_get):
    requests_get.return_value.status_code = status.HTTP_401_UNAUTHORIZED
    with pytest.raises(Unauthorized):
        facade.google_auth(google_token)


def test_google_auth_authenticate(
    google_token, user_email, requests_get, success_response, authenticate_mocked
):
    requests_get.return_value.text = success_response
    facade.google_auth(google_token)
    authenticate_mocked.assert_called_once_with(user_email)


def test_authentication_not_allowed(faker):
    with pytest.raises(UserNotAllowed):
        facade.authenticate(faker.email())


def test_must_authenticate(user, refresh_token, token_data):
    assert facade.authenticate(user.email) == {
        'useremail': user.email,
        'access_token': token_data['access_token'],
        'refresh_token': token_data['refresh_token'],
    }

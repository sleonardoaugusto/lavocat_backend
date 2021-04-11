import pytest
from django.contrib.auth.models import User
from rest_framework import status

from lavocat.api.v1.core import facade
from lavocat.api.v1.core.facade import GOOGLE_AUTH_URL, Unauthorized, UserNotAllowed


def test_google_auth_unauthorized(google_token, requests_get):
    requests_get.return_value.status_code = status.HTTP_401_UNAUTHORIZED
    with pytest.raises(Unauthorized):
        facade.google_auth(google_token)


def test_must_call_get_with_params(
    google_token, requests_get, success_response, mocker_authenticate
):
    facade.google_auth(google_token)
    requests_get.assert_called_once_with(
        GOOGLE_AUTH_URL, params={'access_token': google_token}
    )


def test_google_auth_authenticate(
    google_token, user_email, success_response, mocker_authenticate
):
    facade.google_auth(google_token)
    mocker_authenticate.assert_called_once_with(user_email)


def test_authentication_not_allowed(faker):
    with pytest.raises(UserNotAllowed):
        facade.authenticate(faker.email())


def test_must_authenticate(user, refreshed_token, token_data):
    token = facade.authenticate(user.email)
    assert token == {
        'useremail': user.email,
        'access_token': token_data['access_token'],
        'refresh_token': token_data['refresh_token'],
    }


def test_must_create_user_and_authenticate(
    user_allowed_not_registered, refreshed_token, token_data
):
    email = user_allowed_not_registered.email
    token = facade.authenticate(email)

    assert User.objects.filter(email=email).exists()
    assert token == {
        'useremail': email,
        'access_token': token_data['access_token'],
        'refresh_token': token_data['refresh_token'],
    }

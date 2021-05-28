import json

import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from lavocat.api.v1.core.facade import UserNotAllowed, Unauthorized


@pytest.fixture
def post_authenticate_mock(client, google_auth_mock, google_token):
    return client.post(
        reverse('api-v1:google-auth-list'),
        json.dumps({'token': google_token}),
        content_type='application/json',
    )


def test_should_call_action(post_authenticate_mock, google_auth_mock, google_token):
    google_auth_mock.assert_called_once_with(google_token)


@pytest.fixture
def post_authenticate_not_allowed(client, google_auth_mock, google_token):
    google_auth_mock.side_effect = UserNotAllowed
    return client.post(
        reverse('api-v1:google-auth-list'),
        json.dumps({'token': google_token}),
        content_type='application/json',
    )


def test_not_allowed(post_authenticate_not_allowed):
    assert post_authenticate_not_allowed.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.fixture
def post_authenticate_unauthorized(client, google_auth_mock, google_token):
    google_auth_mock.side_effect = Unauthorized
    return client.post(
        reverse('api-v1:google-auth-list'),
        json.dumps({'token': google_token}),
        content_type='application/json',
    )


def test_unauthorized(post_authenticate_unauthorized):
    assert post_authenticate_unauthorized.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.fixture
def response_content_authorized(token_data, user_email):
    return {
        'useremail': user_email,
        'access_token': token_data['access_token'],
        'refresh_token': token_data['refresh_token'],
    }


@pytest.fixture
def post_authenticate_authorized(
    client, google_auth_mock, response_content_authorized, google_token
):
    google_auth_mock.return_value = response_content_authorized
    return client.post(
        reverse('api-v1:google-auth-list'),
        json.dumps({'token': google_token}),
        content_type='application/json',
    )


def test_authorized(post_authenticate_authorized, response_content_authorized):
    assert post_authenticate_authorized.status_code == status.HTTP_200_OK
    assert post_authenticate_authorized.json() == response_content_authorized

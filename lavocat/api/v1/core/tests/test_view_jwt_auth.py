import json

import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse


@pytest.fixture
def post_unauthorized(client_unauthenticated, faker):
    data = dict(username=faker.name(), password=faker.password())
    return client_unauthenticated.post(
        reverse('api-v1:jwt-auth'),
        json.dumps(data),
        content_type='application/json',
    )


def test_unauthorized_access(post_unauthorized):
    assert post_unauthorized.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.fixture
def post_authorized(client_unauthenticated, faker):
    data = dict(username=faker.name(), password=faker.name())
    User.objects.create_user(**data)
    return client_unauthenticated.post(
        reverse('api-v1:jwt-auth'),
        json.dumps(data),
        content_type='application/json',
    )


def test_status_code(post_authorized):
    assert post_authorized.status_code == status.HTTP_200_OK


def test_content(post_authorized):
    access_token_len = 205
    refresh_token_len = 207
    assert len(post_authorized.json()['access']) == access_token_len
    assert len(post_authorized.json()['refresh']) == refresh_token_len

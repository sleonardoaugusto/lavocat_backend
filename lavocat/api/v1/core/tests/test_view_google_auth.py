import pytest
from rest_framework import status
from rest_framework.reverse import reverse


@pytest.fixture
def response(client):
    return client.post(reverse('api-v1:google-auth'))


def test_status_code(response):
    assert response.status_code == status.HTTP_200_OK

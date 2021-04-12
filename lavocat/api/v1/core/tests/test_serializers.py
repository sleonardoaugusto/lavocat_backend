import pytest

from lavocat.api.v1.core.serializers import GoogleAuthSerializer


@pytest.fixture
def google_auth_serializer_data(faker):
    return dict(token=faker.uuid4())


@pytest.fixture
def google_auth_serializer(google_auth_serializer_data):
    return GoogleAuthSerializer(google_auth_serializer_data)


def test_google_auth_serializer_fields(google_auth_serializer):
    assert google_auth_serializer.data.keys() == {'token'}


def test_google_auth_serializer_values(
    google_auth_serializer, google_auth_serializer_data
):
    assert google_auth_serializer.data['token'] == google_auth_serializer_data['token']

from pathlib import Path

import pytest
from faker import Faker
from model_bakery import baker
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from lavocat.attendances.models import AttendanceFile


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def client():
    user = baker.make('User')
    token = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')
    return client


@pytest.fixture
def delete_file():
    yield
    af = AttendanceFile.objects.all().first()
    path = Path(af.file.path)
    path.unlink()
    path.parent.rmdir()


@pytest.fixture
def faker():
    return Faker('pt-BR')

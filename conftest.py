from pathlib import Path

import pytest
from faker import Faker
from rest_framework.test import APIClient

from lavocat.attendances.models import AttendanceFile


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def client():
    return APIClient()


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

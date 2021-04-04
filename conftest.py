from pathlib import Path

import pytest
from rest_framework.test import APIClient

from lavocat.attendances.models import AttendanceFile


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

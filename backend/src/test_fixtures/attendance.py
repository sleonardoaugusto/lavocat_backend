import pytest
from django.core.files.storage import FileSystemStorage
from model_bakery import baker

from src.attendances.models import (
    ServicesTypesOptions,
    AttendanceFile,
    Attendance,
    AttendanceStatus,
)


@pytest.fixture
def attendance() -> Attendance:
    return baker.make(
        'Attendance',
        customer_name='Natalino Dingoubel',
        document_id='45009877899',
        status=AttendanceStatus.PENDING_DOCS,
    )


@pytest.fixture
def attendances():
    params = [
        dict(
            customer_name='Maria',
            document_id='99999999999',
            services_types=ServicesTypesOptions.DPVAT,
        ),
        dict(
            customer_name='Mara',
            document_id='11199999999',
            services_types=ServicesTypesOptions.AUXILIO_DOENCA,
        ),
        dict(
            customer_name='Faria',
            document_id='11999999999',
            services_types=ServicesTypesOptions.AUXILIO_ACIDENTE,
        ),
    ]
    return [baker.make('Attendance', **p) for p in params]


@pytest.fixture
def attendance_file(attendance, delete_file) -> AttendanceFile:
    AttendanceFile.file.field.storage = FileSystemStorage()
    yield baker.make('AttendanceFile', _create_files=True, attendance=attendance)

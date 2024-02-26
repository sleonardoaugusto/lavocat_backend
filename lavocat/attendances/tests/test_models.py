import pytest
from django.core.files.storage import FileSystemStorage
from django.db.models.fields.files import FieldFile
from model_bakery import baker

from lavocat.attendances.models import Attendance, AttendanceFile


def test_should_exist_attendance_model(attendance):
    assert Attendance.objects.all().count() == 1


@pytest.fixture
def attendance_file(delete_file):
    AttendanceFile.file.field.storage = FileSystemStorage()
    return baker.make('AttendanceFile', _create_files=True)


def test_should_exist_attendance_file(attendance_file):
    assert Attendance.objects.all().count() == 1


def test_attribute_attendance_file(attendance_file):
    record = baker.make('AttendanceFile')
    assert isinstance(record.attendance, Attendance)
    assert isinstance(record.file, FieldFile)

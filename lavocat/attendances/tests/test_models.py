import pytest
from django.core.files.storage import FileSystemStorage
from django.db.models.fields.files import FieldFile
from model_bakery import baker

from lavocat.attendances.models import Attendance, AttendanceStatus, AttendanceFile


@pytest.mark.django_db
class TestAttendanceModel:
    def test_must_exist(self):
        baker.make(
            'Attendance',
            customer_name='Natalino Dingoubel',
            document_id=45009877899,
            status=AttendanceStatus.PENDING_DOCS,
        )
        assert Attendance.objects.all().count() == 1


@pytest.mark.django_db
class TestAttendanceFileModel:
    @pytest.fixture(autouse=True)
    def record(self, delete_file):
        AttendanceFile.file.field.storage = FileSystemStorage()
        return baker.make('AttendanceFile', _create_files=True)

    def test_must_exist(self):
        assert Attendance.objects.all().count() == 1

    def test_attributes(self):
        record = baker.make('AttendanceFile')
        assert isinstance(record.attendance, Attendance)
        assert isinstance(record.file, FieldFile)

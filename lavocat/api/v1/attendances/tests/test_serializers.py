from pathlib import Path, PurePath

from django.core.files.storage import FileSystemStorage
from django.test import TestCase
from model_bakery import baker

from lavocat.api.v1.attendances.serializers import (
    AttendanceSerializer,
    AttendanceFileSerializer,
)
from lavocat.attendances.models import AttendanceFile


class AttendanceSerializerData(TestCase):
    def setUp(self) -> None:
        self.attendance = baker.make('Attendance', _fill_optional=True)
        self.files = baker.make('AttendanceFile', attendance=self.attendance)
        self.serializer = AttendanceSerializer(self.attendance)

    def test_fields(self):
        values = (
            ('id', self.attendance.pk),
            ('customer_name', self.attendance.customer_name),
            ('document_id', self.attendance.document_id),
            ('status', self.attendance.status),
            ('resume', self.attendance.resume),
        )

        for attr, value in values:
            with self.subTest():
                self.assertEqual(self.serializer.data[attr], value)


class AttendanceSerializerValidationsTest(TestCase):
    def test_document_id_length(self):
        data = dict(customer_name='Valeu Natalina', document_id='9999999999')
        serializer = AttendanceSerializer(data=data)

        self.assertValidationErrorCode(serializer, 'document_id', 'length')

    def assertValidationErrorCode(self, serializer, field, code):
        serializer.is_valid()

        errors = serializer.errors
        errors_list = errors[field]
        exception = errors_list[0]

        self.assertEqual(exception.code, code)


class AttendanceFileSerializerData(TestCase):
    def setUp(self) -> None:
        AttendanceFile.file.field.storage = FileSystemStorage()
        self.record = baker.make('AttendanceFile', _create_files=True)
        self.serializer_data = AttendanceFileSerializer(self.record).data

    def tearDown(self) -> None:
        af = AttendanceFile.objects.all().first()
        path = Path(af.file.path)

        def delete_file_and_dir():
            path.unlink()
            path.parent.rmdir()

        delete_file_and_dir()

    def test_field_values(self):
        self.assertEqual(
            set(self.serializer_data.keys()), {'id', 'file', 'attendance', 'filename'}
        )
        self.assertEqual(self.serializer_data['file'], f'/{self.record.file.name}')
        self.assertEqual(
            self.serializer_data['filename'], self.get_file_name(self.record)
        )

    @staticmethod
    def get_file_name(record):
        return PurePath(record.file.name).name

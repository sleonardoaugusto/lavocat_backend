from django.test import TestCase
from model_bakery import baker

from lavocat.api.v1.attendances.serializers import (
    AttendanceSerializer,
    AttendanceFileSerializer,
)


class AttendanceSerializerData(TestCase):
    def setUp(self) -> None:
        attendance = baker.prepare('Attendance')
        self.serializer = AttendanceSerializer(attendance)

    def test_attributes(self):
        self.assertEqual(
            set(self.serializer.data.keys()),
            {'id', 'customer_name', 'document_id', 'files', 'status'},
        )


class AttendanceSerializerValidationsTest(TestCase):
    def test_document_id_length(self):
        data = dict(customer_name='Valeu Natalina', document_id=9999999999)
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
        attendance_file = baker.prepare('AttendanceFile')
        self.serializer = AttendanceFileSerializer(attendance_file)

    def test_fields(self):
        self.assertEqual(set(self.serializer.data.keys()), {'id', 'file', 'attendance'})

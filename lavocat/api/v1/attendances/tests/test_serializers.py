from django.test import TestCase
from model_bakery import baker

from lavocat.api.v1.attendances.serializers import (
    AttendanceSerializer,
    AttachmentSerializer,
)


class AttendanceSerializerData(TestCase):
    def setUp(self) -> None:
        attendance = baker.prepare('Attendance')
        self.serializer = AttendanceSerializer(attendance)

    def test_data(self):
        self.assertEqual(
            set(self.serializer.data.keys()), {'id', 'customer_name', 'document_id'}
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


class AttachmentSerializerData(TestCase):
    def setUp(self) -> None:
        attachment = baker.prepare('Attachment')
        self.serializer = AttachmentSerializer(attachment)

    def test_fields(self):
        self.assertEqual(set(self.serializer.data.keys()), {'id', 'file', 'attendance'})

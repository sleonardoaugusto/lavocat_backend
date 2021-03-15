from django.test import TestCase

from lavocat.api.v1.attendances.serializers import AttendanceSerializer


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

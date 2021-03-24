from django.db.models.fields.files import FieldFile
from django.test import TestCase
from model_bakery import baker

from lavocat.attendances.models import Attendance, AttendanceStatus


class AttendanceModelTest(TestCase):
    def setUp(self) -> None:
        self.attendance = baker.make(
            'Attendance',
            customer_name='Natalino Dingoubel',
            document_id=45009877899,
            status=AttendanceStatus.PENDING_DOCS,
        )

    def test_create(self):
        self.assertEqual(Attendance.objects.all().count(), 1)


class AttendanceFileModelTest(TestCase):
    def setUp(self) -> None:
        self.attendance_file = baker.make('AttendanceFile')

    def test_attributes(self):
        self.assertIsInstance(self.attendance_file.attendance, Attendance)
        self.assertIsInstance(self.attendance_file.file, FieldFile)

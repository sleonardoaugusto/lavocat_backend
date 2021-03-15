from django.db.models.fields.files import FieldFile
from django.test import TestCase
from model_bakery import baker

from lavocat.attendances.models import Attendance


class AttendanceModelTest(TestCase):
    def setUp(self) -> None:
        self.attendance = baker.make(
            'Attendance', customer_name='Natalino Dingoubel', document_id=45009877899
        )

    def test_must_exist(self):
        self.assertEqual(Attendance.objects.all().count(), 1)

    def test_attributes(self):
        self.assertEqual(self.attendance.customer_name, 'Natalino Dingoubel')
        self.assertEqual(self.attendance.document_id, 45009877899)


class AttendanceFileModelTest(TestCase):
    def setUp(self) -> None:
        self.attendance_file = baker.make('AttendanceFile')

    def test_attributes(self):
        self.assertIsInstance(self.attendance_file.attendance, Attendance)
        self.assertIsInstance(self.attendance_file.file, FieldFile)

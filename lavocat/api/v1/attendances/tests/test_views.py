from pathlib import Path, PurePath
from time import time
from unittest import mock

from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.test import TestCase
from model_bakery import baker
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from lavocat.api.v1.attendances.serializers import (
    AttendanceSerializer,
    AttendanceFileSerializer,
)
from lavocat.attendances.models import Attendance, AttendanceFile, AttendanceStatus


class Client:
    client = APIClient()


class AttendanceViewsetGetTest(TestCase, Client):
    def setUp(self) -> None:
        self.resp = self.client.get(reverse('api-v1:attendance-list'))

    def test_url(self):
        self.assertEqual(self.resp.status_code, status.HTTP_200_OK)


class AttendanceViewsetPostTest(TestCase, Client):
    def setUp(self) -> None:
        data = dict(
            customer_name='Valeu Natalina',
            document_id=99999999999,
            status=AttendanceStatus.PENDING_DOCS,
        )
        attendance = baker.prepare('Attendance', **data)
        self.serializer = AttendanceSerializer
        payload = self.serializer(attendance).data
        self.resp = self.client.post(
            reverse('api-v1:attendance-list'),
            payload,
            content_type='application/json',
        )

    def test_must_exist(self):
        self.assertEqual(Attendance.objects.all().count(), 1)

    def test_status_returned(self):
        self.assertEqual(self.resp.status_code, status.HTTP_201_CREATED)

    def test_content_returned(self):
        expect = self.serializer(Attendance.objects.all().first()).data

        self.assertDictEqual(self.resp.json(), expect)


class AttendanceFileViewsetGetTest(TestCase, Client):
    def setUp(self) -> None:
        self.resp = self.client.get(reverse('api-v1:attendancefile-list'))

    def test_url(self):
        self.assertEqual(self.resp.status_code, status.HTTP_200_OK)


class AttendanceFileViewsetPostTest(TestCase, Client):
    def setUp(self) -> None:
        AttendanceFile.file.field.storage = FileSystemStorage()
        self.serializer = AttendanceFileSerializer
        attendance = baker.make('Attendance')
        payload = {'attendance': attendance.pk, 'file': self.mock_file()}
        self.resp = self.client.post(reverse('api-v1:attendancefile-list'), payload)

    def tearDown(self) -> None:
        af = AttendanceFile.objects.all().first()
        path = Path(af.file.path)

        def delete_file_and_dir():
            path.unlink()
            path.parent.rmdir()

        delete_file_and_dir()

    def test_must_exist(self):
        self.assertEqual(AttendanceFile.objects.all().count(), 1)

    def test_status_returned(self):
        self.assertEqual(self.resp.status_code, status.HTTP_201_CREATED)

    def test_content_returned(self):
        record = AttendanceFile.objects.all().first()
        expect = {
            'id': record.pk,
            'attendance': record.attendance.pk,
            'file': self._get_file_url(record.file.url),
            'filename': PurePath(record.file.name).name,
        }

        self.assertDictEqual(self.resp.json(), expect)

    def mock_file(self):
        self.fname = f'{int(str(time()).replace(".", ""))}.doc'
        file_mock = mock.Mock(spec=File)
        file_mock.name = self.fname
        return file_mock

    @staticmethod
    def _get_file_url(fpath):
        return f'http://testserver{fpath}'


class AttendanceStatusesViewTest(TestCase):
    def setUp(self) -> None:
        self.resp = self.client.get(reverse('api-v1:attendance-statuses'))

    def test_get(self):
        self.assertEqual(self.resp.status_code, status.HTTP_200_OK)

    def test_data(self):
        expect = {
            'Documentação Pendente': 1,
            'Documentação Parcial': 2,
            'À Contatar': 3,
            'Concluído': 4,
        }

        self.assertDictEqual(self.resp.json(), expect)

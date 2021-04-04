import json
from pathlib import PurePath
from time import time
from unittest import mock

import pytest
from django.core.files import File
from model_bakery import baker
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from lavocat.api.v1.attendances.serializers import (
    AttendanceSerializer,
)
from lavocat.attendances.models import Attendance, AttendanceFile, AttendanceStatus


class Client:
    client = APIClient()


@pytest.mark.django_db
class TestAttendanceViewsetGet:
    def test_get(self, client):
        resp = client.get(reverse('api-v1:attendance-list'))
        assert resp.status_code, status.HTTP_200_OK


@pytest.mark.django_db
class TestAttendanceViewsetPost:
    @pytest.fixture(autouse=True)
    def response(self, client):
        attendance = baker.prepare(
            'Attendance',
            customer_name='Valeu Natalina',
            document_id=99999999999,
            status=AttendanceStatus.PENDING_DOCS,
        )
        payload = AttendanceSerializer(attendance).data
        return client.post(
            reverse('api-v1:attendance-list'),
            json.dumps(payload),
            content_type='application/json',
        )

    def test_must_exist(self, response):
        assert Attendance.objects.all().count() == 1

    def test_status_returned(self, response):
        assert response.status_code == status.HTTP_201_CREATED

    def test_content_returned(self, response):
        expect = AttendanceSerializer(Attendance.objects.all().first()).data
        assert response.json() == expect


@pytest.mark.django_db
class TestAttendanceViewsetQuerystring:
    @pytest.fixture(autouse=True)
    def factory(self):
        params = [
            dict(
                customer_name='Maria',
                document_id='99999999999',
                status=AttendanceStatus.PENDING_DOCS,
            ),
            dict(
                customer_name='Mara',
                document_id='11199999999',
                status=AttendanceStatus.DONE,
            ),
            dict(
                customer_name='Faria',
                document_id='11999999999',
                status=AttendanceStatus.TO_CONTACT,
            ),
        ]
        [baker.make('Attendance', **p) for p in params]

    def test_name_filter(self, client):
        qs = '?customer_name=ara'
        resp = client.get(f"{reverse('api-v1:attendance-list')}{qs}")
        data = resp.json()
        assert len(data) == 1

    def test_document_filter(self, client):
        qs = '?document_id=111'
        resp = client.get(f"{reverse('api-v1:attendance-list')}{qs}")
        data = resp.json()
        assert len(data) == 1

    def test_status_filter(self, client):
        qs = f'?status={AttendanceStatus.DONE}&status={AttendanceStatus.PENDING_DOCS}'
        resp = client.get(f"{reverse('api-v1:attendance-list')}{qs}")
        data = resp.json()
        assert len(data) == 2


@pytest.mark.django_db
class TestAttendanceFileViewsetGet:
    def test_url(self, client):
        response = client.get(reverse('api-v1:attendancefile-list'))
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestAttendanceFileViewsetPost:
    @pytest.fixture(autouse=True)
    def response(self, client, delete_file):
        attendance = baker.make('Attendance')
        payload = {'attendance': attendance.pk, 'file': self.mock_file()}
        return client.post(reverse('api-v1:attendancefile-list'), payload)

    def test_must_exist(self):
        assert AttendanceFile.objects.all().count() == 1

    def test_status_returned(self, response):
        assert response.status_code == status.HTTP_201_CREATED

    def mock_file(self):
        self.fname = f'{int(str(time()).replace(".", ""))}.doc'
        file_mock = mock.Mock(spec=File)
        file_mock.name = self.fname
        return file_mock

    def test_content_returned(self, response):
        record = AttendanceFile.objects.all().first()
        expect = {
            'id': record.pk,
            'attendance': record.attendance.pk,
            'file': self._get_file_url(record.file.url),
            'filename': PurePath(record.file.name).name,
        }
        assert response.json() == expect

    @staticmethod
    def _get_file_url(fpath):
        return f'http://testserver{fpath}'


@pytest.mark.django_db
class TestAttendanceStatusesView:
    @pytest.fixture
    def response(self, client):
        return client.get(reverse('api-v1:attendance-statuses'))

    def test_content(self, response):
        expect = {
            'Documentação pendente': 1,
            'Em andamento': 2,
            'À contatar': 3,
            'Concluído': 4,
        }
        assert response.json() == expect

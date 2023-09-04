import json

import pytest
from model_bakery import baker
from rest_framework import status
from rest_framework.reverse import reverse

from lavocat.api.v1.attendances.serializers import (
    AttendanceSerializer,
)
from lavocat.attendances.models import (
    Attendance,
    AttendanceFile,
    AttendanceStatus,
    ServicesTypesOptions,
)


class TestAttendanceEndpoints:
    @staticmethod
    def test_get_attendance(client):
        baker.make("Attendance")
        resp = client.get(reverse('api-v1:attendance-list'))
        assert resp.status_code, status.HTTP_200_OK
        assert set(resp.json()[0]) == {
            'customer_name',
            'document_id',
            'files',
            'id',
            'resume',
            'services_types',
            'status_resume',
        }

    @staticmethod
    def test_post_attendance(client):
        attendance = baker.prepare(
            'Attendance',
            customer_name='Valeu Natalina',
            document_id=99999999999,
            status=AttendanceStatus.PENDING_DOCS,
            resume='Resume description',
            status_resume='Status resume description',
        )
        payload = AttendanceSerializer(attendance).data
        response = client.post(
            reverse('api-v1:attendance-list'),
            json.dumps(payload),
            content_type='application/json',
        )
        assert Attendance.objects.all().count() == 1
        assert response.status_code == status.HTTP_201_CREATED
        assert set(response.json()) == {
            'customer_name',
            'document_id',
            'files',
            'id',
            'resume',
            'services_types',
            'status_resume',
        }

    @staticmethod
    def test_delete_attendance(client):
        attendance_file = baker.make('AttendanceFile')
        resp = client.delete(
            reverse('api-v1:attendance-detail', args=[attendance_file.attendance.pk])
        )
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert Attendance.objects.all().count() == 0


class TestAttendanceFilters:
    @staticmethod
    @pytest.fixture
    def attendances():
        params = [
            dict(
                customer_name='Maria',
                document_id='99999999999',
                services_types=ServicesTypesOptions.DPVAT,
            ),
            dict(
                customer_name='Mara',
                document_id='11199999999',
                services_types=ServicesTypesOptions.AUXILIO_DOENCA,
            ),
            dict(
                customer_name='Faria',
                document_id='11999999999',
                services_types=ServicesTypesOptions.AUXILIO_ACIDENTE,
            ),
        ]
        [baker.make('Attendance', **p) for p in params]

    @staticmethod
    def test_filter_by_attendance_name(attendances, client):
        qs = '?customer_name=ara'
        resp = client.get(f"{reverse('api-v1:attendance-list')}{qs}")
        data = resp.json()
        assert len(data) == 1

    @staticmethod
    def test_filter_by_attendance_document(attendances, client):
        qs = '?document_id=111'
        resp = client.get(f"{reverse('api-v1:attendance-list')}{qs}")
        data = resp.json()
        assert len(data) == 1

    @staticmethod
    def test_filter_by_attendance_status(attendances, client):
        qs = f'?status={AttendanceStatus.DONE}&status={AttendanceStatus.PENDING_DOCS}'
        resp = client.get(f"{reverse('api-v1:attendance-list')}{qs}")
        data = resp.json()
        assert len(data) == 2


class TestAttendanceFileEndpoint:
    @staticmethod
    def test_get_attendance_file(client):
        response = client.get(reverse('api-v1:attendancefile-list'))
        assert response.status_code == status.HTTP_200_OK

    @staticmethod
    def test_post_attendance_file(client, delete_file, file):
        attendance = baker.make('Attendance')
        payload = {'attendance': attendance.pk, 'file': file, 'filename': file.name}
        resp = client.post(reverse('api-v1:attendancefile-list'), payload)
        attendance_file = AttendanceFile.objects.first()
        assert AttendanceFile.objects.all().count() == 1
        assert resp.status_code == status.HTTP_201_CREATED
        assert attendance_file.filename == 'file.txt'

    @staticmethod
    def test_update_filename(client, delete_file, file):
        attendance_file = baker.make(
            'AttendanceFile',
            file=file,
            attendance=baker.make('Attendance', _fill_optional=True),
        )
        resp = client.patch(
            reverse('api-v1:attendancefile-detail', args=[attendance_file.pk]),
            data={"filename": "new-name.pdf"},
        )
        attendance_file.refresh_from_db()
        assert resp.status_code == status.HTTP_200_OK
        assert attendance_file.filename == 'new-name.pdf'


def test_get_attendance_statuses(client):
    resp = client.get(reverse('api-v1:attendance-statuses'))
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == {
        'Documentação pendente': 1,
        'Em andamento': 2,
        'À contatar': 3,
        'Concluído': 4,
    }


class TestAttendanceFilesNestedView:
    @staticmethod
    def test_list_attendance_files_by_application(client):
        attendance_file = baker.make('AttendanceFile')
        baker.make("AttendanceFile")
        url = reverse(
            'api-v1:attendance-attendance-file-list',
            kwargs={'attendance_pk': attendance_file.attendance.pk},
        )
        resp = client.get(url)
        assert resp.status_code == status.HTTP_200_OK
        assert len(resp.json()) == 1
        assert set(resp.json()[0]) == {
            'attendance',
            'file',
            'id',
            'filename',
        }

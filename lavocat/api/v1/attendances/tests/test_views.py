import json
from pathlib import PurePath
from time import time
from unittest import mock

import pytest
from django.core.files import File
from model_bakery import baker
from rest_framework import status
from rest_framework.reverse import reverse

from lavocat.api.v1.attendances.serializers import (
    AttendanceSerializer,
)
from lavocat.attendances.models import Attendance, AttendanceFile, AttendanceStatus


def test_get_attendance_viewset(client):
    resp = client.get(reverse('api-v1:attendance-list'))
    assert resp.status_code, status.HTTP_200_OK


@pytest.fixture
def post_attendance_response(client):
    attendance = baker.prepare(
        'Attendance',
        customer_name='Valeu Natalina',
        document_id=99999999999,
        status=AttendanceStatus.PENDING_DOCS,
        resume='Resume description',
        status_resume='Status resume description',
    )
    payload = AttendanceSerializer(attendance).data
    return client.post(
        reverse('api-v1:attendance-list'),
        json.dumps(payload),
        content_type='application/json',
    )


def test_attendance_should_exist(post_attendance_response):
    assert Attendance.objects.all().count() == 1


def test_attendance_status_response(post_attendance_response):
    assert post_attendance_response.status_code == status.HTTP_201_CREATED


def test_attendance_content_response(post_attendance_response):
    assert post_attendance_response.json() == {
        'customer_name': 'Valeu Natalina',
        'document_id': '99999999999',
        'files': [],
        'id': 1,
        'resume': 'Resume description',
        'status': 1,
        'status_label': 'Documentação pendente',
        'status_resume': 'Status resume description',
    }


def test_attendance_delete(client):
    attendance_file = baker.make('AttendanceFile')
    resp = client.delete(
        reverse('api-v1:attendance-detail', args=[attendance_file.attendance.pk])
    )
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    assert Attendance.objects.all().count() == 0


@pytest.fixture
def attendances():
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


def test_filter_by_attendance_name(attendances, client):
    qs = '?customer_name=ara'
    resp = client.get(f"{reverse('api-v1:attendance-list')}{qs}")
    data = resp.json()
    assert len(data) == 1


def test_filter_by_attendance_document(attendances, client):
    qs = '?document_id=111'
    resp = client.get(f"{reverse('api-v1:attendance-list')}{qs}")
    data = resp.json()
    assert len(data) == 1


def test_filter_by_attendance_status(attendances, client):
    qs = f'?status={AttendanceStatus.DONE}&status={AttendanceStatus.PENDING_DOCS}'
    resp = client.get(f"{reverse('api-v1:attendance-list')}{qs}")
    data = resp.json()
    assert len(data) == 2


def test_get_attendance_file_viewset(client):
    response = client.get(reverse('api-v1:attendancefile-list'))
    assert response.status_code == status.HTTP_200_OK


@pytest.fixture
def post_attendance_file(client, delete_file):
    attendance = baker.make('Attendance')
    payload = {'attendance': attendance.pk, 'file': mock_file()}
    return client.post(reverse('api-v1:attendancefile-list'), payload)


def test_attendance_file_should_exist(post_attendance_file):
    assert AttendanceFile.objects.all().count() == 1


def test_attendance_file_status_response(post_attendance_file):
    assert post_attendance_file.status_code == status.HTTP_201_CREATED


def test_attendance_file_content_returned(post_attendance_file):
    record = AttendanceFile.objects.all().first()
    expect = {
        'id': record.pk,
        'attendance': record.attendance.pk,
        'file': _get_file_url(record.file.url),
        'filename': PurePath(record.file.name).name,
    }
    assert post_attendance_file.json() == expect


def mock_file():
    fname = f'{int(str(time()).replace(".", ""))}.doc'
    file_mock = mock.Mock(spec=File)
    file_mock.name = fname
    return file_mock


def _get_file_url(fpath):
    return f'http://testserver{fpath}'


@pytest.fixture
def attendance_statuses_response(client):
    return client.get(reverse('api-v1:attendance-statuses'))


def test_status_code(attendance_statuses_response):
    assert attendance_statuses_response.status_code == status.HTTP_200_OK


def test_content(attendance_statuses_response):
    expect = {
        'Documentação pendente': 1,
        'Em andamento': 2,
        'À contatar': 3,
        'Concluído': 4,
    }
    assert attendance_statuses_response.json() == expect

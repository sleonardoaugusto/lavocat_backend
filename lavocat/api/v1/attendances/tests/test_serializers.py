from pathlib import PurePath

import pytest
from django.core.files.storage import FileSystemStorage
from model_bakery import baker

from lavocat.api.v1.attendances.serializers import (
    AttendanceSerializer,
    AttendanceFileSerializer,
)
from lavocat.attendances.models import AttendanceStatus, AttendanceFile
from lavocat.custom_assertions import assert_validation_error_code


@pytest.fixture
def attendance():
    return baker.make('Attendance', _fill_optional=True)


@pytest.fixture
def attendance_file(attendance, delete_file):
    AttendanceFile.file.field.storage = FileSystemStorage()
    yield baker.make('AttendanceFile', _create_files=True, attendance=attendance)


@pytest.fixture
def attendance_serializer(attendance_file):
    return AttendanceSerializer(attendance_file.attendance)


@pytest.fixture
def attendance_file_serializer(attendance_file):
    return AttendanceFileSerializer(attendance_file)


def test_fields_attendance_serializer(attendance_serializer):
    data = attendance_serializer.data
    assert set(data.keys()) == {
        'id',
        'customer_name',
        'document_id',
        'files',
        'status',
        'status_label',
        'resume',
        'status_resume',
    }


def test_values_attendance_serializer(attendance_serializer, attendance):
    values = (
        ('id', attendance.pk),
        ('customer_name', attendance.customer_name),
        ('document_id', attendance.document_id),
        ('status', attendance.status),
        ('status_label', AttendanceStatus(attendance.status).label),
        ('resume', attendance.resume),
        ('status_resume', attendance.status_resume),
    )
    for attr, value in values:
        assert attendance_serializer.data[attr] == value


def test_document_id_length():
    data = dict(customer_name='Valeu Natalina', document_id='9999999999')
    serializer = AttendanceSerializer(data=data)
    assert_validation_error_code(serializer, 'document_id', 'length')


def test_fields_attendance_file_serializer(attendance_file_serializer):
    assert set(attendance_file_serializer.data.keys()) == {
        'id',
        'file',
        'attendance',
        'filename',
    }


def test_values_attendance_file_serializer(attendance_file, attendance_file_serializer):
    assert (
        attendance_file_serializer.data['file']
        == f'/mediafiles/{attendance_file.file.name}'
    )
    assert attendance_file_serializer.data['filename'] == get_file_name(attendance_file)


def get_file_name(record):
    return PurePath(record.file.name).name

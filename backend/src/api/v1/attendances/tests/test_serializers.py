import pytest

from src.api.v1.attendances.serializers import (
    AttendanceSerializer,
    AttendanceFileSerializer,
    NoteSerializer,
)
from src.custom_assertions import assert_validation_error_code


@pytest.fixture
def attendance_serializer(attendance_file):
    return AttendanceSerializer(attendance_file.attendance)


@pytest.fixture
def attendance_file_serializer(attendance_file):
    return AttendanceFileSerializer(attendance_file)


@pytest.fixture
def note_serializer(note):
    return NoteSerializer(note)


class TestAttendanceSerializer:
    @staticmethod
    def test_fields_attendance_serializer(attendance_serializer):
        data = attendance_serializer.data
        assert set(data.keys()) == {
            'id',
            'customer_name',
            'source',
            'document_id',
            'files',
            'resume',
            'services_types',
            'status_resume',
            'is_client',
            'created_at',
        }

    @staticmethod
    def test_values_attendance_serializer(attendance_serializer, attendance):
        values = (
            ('id', attendance.pk),
            ('customer_name', attendance.customer_name),
            ('document_id', attendance.document_id),
            ('resume', attendance.resume),
            ('status_resume', attendance.status_resume),
        )
        for attr, value in values:
            assert attendance_serializer.data[attr] == value

    @staticmethod
    def test_document_id_length():
        data = dict(customer_name='Valeu Natalina', document_id='9999999999')
        serializer = AttendanceSerializer(data=data)
        assert_validation_error_code(serializer, 'document_id', 'length')


class TestAttendanceFileSerializer:
    @staticmethod
    def test_fields_attendance_file_serializer(attendance_file_serializer):
        assert set(attendance_file_serializer.data.keys()) == {
            'id',
            'file',
            'attendance',
            'filename',
        }

    @staticmethod
    def test_values_attendance_file_serializer(
        attendance_file, attendance_file_serializer
    ):
        assert (
            attendance_file_serializer.data['file']
            == f'/mediafiles/{attendance_file.file.name}'
        )
        assert attendance_file_serializer.data['filename'] == attendance_file.filename


class TestNoteSerializer:
    @staticmethod
    def test_fields_note_serializer(note_serializer):
        assert set(note_serializer.data.keys()) == {'content', 'header', 'id'}

    @staticmethod
    def test_values_note_file_serializer(note, note_serializer):
        assert note_serializer.data['content'] == note.content
        assert note_serializer.data['header'] == note.header
        assert note_serializer.data['id'] == note.pk

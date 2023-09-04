from rest_framework import serializers
from rest_framework.fields import MultipleChoiceField

from lavocat.attendances.models import (
    Attendance,
    AttendanceFile,
    AttendanceStatus,
    ServicesOffered,
)


class AttendanceFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceFile
        fields = (
            'id',
            'attendance',
            'file',
            'filename',
        )


class AttendanceSerializer(serializers.ModelSerializer):
    files = AttendanceFileSerializer(many=True, read_only=True)
    services_provided = MultipleChoiceField(
        choices=ServicesOffered.choices, allow_null=True
    )

    class Meta:
        model = Attendance
        fields = (
            'id',
            'customer_name',
            'document_id',
            'files',
            'status',
            'resume',
            'status_resume',
            'services_provided',
        )

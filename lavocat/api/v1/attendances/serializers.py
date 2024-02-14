from rest_framework import serializers
from rest_framework.fields import MultipleChoiceField

from lavocat.attendances.models import (
    Attendance,
    AttendanceFile,
    ServicesTypesOptions,
    Note,
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
    services_types = MultipleChoiceField(
        choices=ServicesTypesOptions.choices, allow_null=True
    )

    class Meta:
        model = Attendance
        fields = (
            'id',
            'customer_name',
            'source',
            'document_id',
            'files',
            'resume',
            'status_resume',
            'services_types',
        )

    def create(self, validated_data):
        instance = super().create(validated_data)
        for service_type in instance.services_types:
            label = ServicesTypesOptions(service_type).label
            Note.objects.create(attendance=instance, header=label)
        return instance


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = (
            'id',
            'header',
            'content',
        )

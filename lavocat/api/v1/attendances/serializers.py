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
            'created_at',
        )

    def create(self, validated_data):
        instance = super().create(validated_data)
        for service_type in instance.services_types:
            label = ServicesTypesOptions(service_type).label
            Note.objects.create(attendance=instance, header=label)
        return instance

    def update(self, instance, validated_data):
        current_services = [
            ServicesTypesOptions(service).label for service in instance.services_types
        ]
        new_services = [
            ServicesTypesOptions(service).label
            for service in validated_data['services_types']
        ]
        to_create = set(new_services) - set(current_services)
        to_delete = set(current_services) - set(new_services)
        Note.objects.filter(attendance=instance, header__in=to_delete).delete()
        Note.objects.bulk_create(
            [Note(attendance=instance, header=service) for service in to_create]
        )
        instance = super().update(instance, validated_data)
        return instance


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = (
            'id',
            'header',
            'content',
        )

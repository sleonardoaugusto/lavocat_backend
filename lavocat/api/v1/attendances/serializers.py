from pathlib import PurePath

from rest_framework import serializers

from lavocat.attendances.models import Attendance, AttendanceFile


class AttendanceFileSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceFile
        fields = (
            'id',
            'attendance',
            'file',
            'filename',
        )

    def get_filename(self, obj):
        return PurePath(obj.file.name).name


class AttendanceSerializer(serializers.ModelSerializer):
    files = AttendanceFileSerializer(many=True, read_only=True)

    class Meta:
        model = Attendance
        fields = (
            'id',
            'customer_name',
            'document_id',
            'files',
            'status',
            'resume',
        )

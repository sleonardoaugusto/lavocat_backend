from rest_framework import serializers

from lavocat.attendances.models import Attendance, AttendanceFile


class AttendanceFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceFile
        fields = (
            'id',
            'attendance',
            'file',
        )


class AttendanceSerializer(serializers.ModelSerializer):
    files = AttendanceFileSerializer(many=True, read_only=True)

    class Meta:
        model = Attendance
        fields = ('id', 'customer_name', 'document_id', 'files')

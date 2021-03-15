from rest_framework import serializers

from lavocat.attendances.models import Attendance, AttendanceFile


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = (
            'id',
            'customer_name',
            'document_id',
        )


class AttendanceFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceFile
        fields = (
            'id',
            'attendance',
            'file',
        )

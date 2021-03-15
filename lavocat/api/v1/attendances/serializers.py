from rest_framework import serializers

from lavocat.attendances.models import Attendance, Attachment


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = (
            'id',
            'customer_name',
            'document_id',
        )


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = (
            'id',
            'attendance',
            'file',
        )

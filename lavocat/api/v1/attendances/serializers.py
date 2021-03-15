from rest_framework import serializers

from lavocat.attendances.models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ('id', 'customer_name', 'document_id')

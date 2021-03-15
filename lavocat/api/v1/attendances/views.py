from rest_framework import viewsets

from lavocat.api.v1.attendances.serializers import AttendanceSerializer
from lavocat.attendances.models import Attendance


class AttendanceViewset(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

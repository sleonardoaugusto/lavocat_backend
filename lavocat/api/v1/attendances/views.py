from rest_framework import viewsets

from lavocat.api.v1.attendances.serializers import (
    AttendanceSerializer,
    AttendanceFileSerializer,
)
from lavocat.attendances.models import Attendance, AttendanceFile


class AttendanceViewset(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


class AttendanceFileViewset(viewsets.ModelViewSet):
    queryset = AttendanceFile.objects.all()
    serializer_class = AttendanceFileSerializer

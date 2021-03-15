from rest_framework import viewsets

from lavocat.api.v1.attendances.serializers import (
    AttendanceSerializer,
    AttachmentSerializer,
)
from lavocat.attendances.models import Attendance, Attachment


class AttendanceViewset(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


class AttachmentViewset(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer

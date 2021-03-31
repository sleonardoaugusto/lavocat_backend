from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, views
from rest_framework.response import Response

from lavocat.api.v1.attendances.filters import AttendanceFilter
from lavocat.api.v1.attendances.serializers import (
    AttendanceSerializer,
    AttendanceFileSerializer,
)
from lavocat.attendances.models import Attendance, AttendanceFile, AttendanceStatus


class AttendanceViewset(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AttendanceFilter


class AttendanceFileViewset(viewsets.ModelViewSet):
    queryset = AttendanceFile.objects.all()
    serializer_class = AttendanceFileSerializer


class AttendanceStatusesView(views.APIView):
    def get(self, request):
        data = {}

        [data.update({text: value}) for value, text in AttendanceStatus.choices]

        return Response(data)

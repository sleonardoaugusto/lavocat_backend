from django.utils.datetime_safe import datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, views
from rest_framework.response import Response

from lavocat.api.v1.attendances.filters import AttendanceFilter
from lavocat.api.v1.attendances.serializers import (
    AttendanceSerializer,
    AttendanceFileSerializer,
    NoteSerializer,
)
from lavocat.attendances.models import (
    Attendance,
    AttendanceFile,
    AttendanceStatus,
    Note,
)


class BaseNestedRouteViewSet(viewsets.ModelViewSet):
    nested_lookup = None

    def get_queryset(self):
        return self.queryset.filter(attendance=self.kwargs[self.nested_lookup])


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AttendanceFilter

    def get_queryset(self):
        date = datetime(year=2024, month=5, day=23)
        if not self.request.user.is_superuser:
            return super().get_queryset().filter(created_at__lte=date)
        return super().get_queryset().filter(created_at__gte=date)


class AttendanceFileViewSet(viewsets.ModelViewSet):
    queryset = AttendanceFile.objects.all()
    serializer_class = AttendanceFileSerializer


class NestedAttendanceFileViewSet(BaseNestedRouteViewSet):
    queryset = AttendanceFile.objects.all()
    serializer_class = AttendanceFileSerializer
    nested_lookup = 'attendance_pk'


class NestedNoteViewSet(BaseNestedRouteViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    nested_lookup = 'attendance_pk'


class AttendanceStatusesView(views.APIView):
    def get(self, request):
        data = {}

        [data.update({text: value}) for value, text in AttendanceStatus.choices]

        return Response(data)

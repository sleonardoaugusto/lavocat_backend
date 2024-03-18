from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from src.api.v1.attendances.views import (
    AttendanceViewSet,
    AttendanceFileViewSet,
    AttendanceStatusesView,
    NestedAttendanceFileViewSet,
    NestedNoteViewSet,
)

router = SimpleRouter()
router.register('attendances', AttendanceViewSet)
router.register('attendance-files', AttendanceFileViewSet)


attendance_router = routers.NestedSimpleRouter(
    router,
    'attendances',
    lookup='attendance',
)
attendance_router.register(
    'attendance-files',
    NestedAttendanceFileViewSet,
    basename='attendance-attendance-file',
)
attendance_router.register(
    'notes',
    NestedNoteViewSet,
    basename='attendance-note',
)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'attendance-statuses/',
        AttendanceStatusesView.as_view(),
        name='attendance-statuses',
    ),
    path('', include(attendance_router.urls)),
]

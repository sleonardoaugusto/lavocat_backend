from django.urls import path, include
from rest_framework.routers import SimpleRouter

from lavocat.api.v1.attendances.views import AttendanceViewset, AttendanceFileViewset

router = SimpleRouter()
router.register('attendances', AttendanceViewset)
router.register('attendance-files', AttendanceFileViewset)

urlpatterns = [
    path('', include(router.urls)),
]

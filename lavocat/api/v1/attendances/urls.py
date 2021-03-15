from django.urls import path, include
from rest_framework.routers import SimpleRouter

from lavocat.api.v1.attendances.views import AttendanceViewset

router = SimpleRouter()
router.register('attendances', AttendanceViewset, basename='attendance')

urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path, include
from rest_framework.routers import SimpleRouter

from lavocat.api.v1.attendances.views import AttendanceViewset, AttachmentViewset

router = SimpleRouter()
router.register('attendances', AttendanceViewset)
router.register('attachments', AttachmentViewset)

urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path, include
from rest_framework.routers import SimpleRouter

from lavocat.api.v1.core.views import GoogleAuthViewset

router = SimpleRouter()
router.register('google-auth', GoogleAuthViewset, basename='google-auth')

urlpatterns = [
    path('', include(router.urls)),
]

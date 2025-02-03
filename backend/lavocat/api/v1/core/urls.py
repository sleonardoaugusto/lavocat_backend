from django.urls import path

from lavocat.api.v1.core.views import TokenObtainPairView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='jwt-auth'),
]

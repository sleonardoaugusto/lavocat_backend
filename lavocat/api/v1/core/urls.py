from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt import views as jwt_views

from lavocat.api.v1.core.views import GoogleAuthViewset

router = SimpleRouter()
router.register('google-auth', GoogleAuthViewset, basename='google-auth')

urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='jwt-auth'),
]

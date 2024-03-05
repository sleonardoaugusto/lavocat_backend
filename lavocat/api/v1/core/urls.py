from django.urls import path
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='jwt-auth'),
]

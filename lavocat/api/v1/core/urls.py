from django.urls import path

from lavocat.api.v1.core import views

urlpatterns = [
    path('google-auth/', views.GoogleAuthView.as_view(), name='google-auth'),
]

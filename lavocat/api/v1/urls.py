from django.urls import path, include

app_name = 'api.v1'

urlpatterns = [
    path('', include('lavocat.api.v1.attendances.urls')),
]

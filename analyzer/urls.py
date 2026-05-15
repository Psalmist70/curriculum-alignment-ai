from django.urls import path
from .views import upload_curriculum, health

urlpatterns = [
    path("upload/", upload_curriculum, name="upload_curriculum"),
    path('health/', health),
]
from django.contrib import admin

from django.urls import (
    path,
    include
)

from django.conf import settings

from django.conf.urls.static import static

from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "status": "running",
        "message": "Curriculum Alignment API is live"
    })

urlpatterns = [
    path("", home),  # 👈 THIS FIXES YOUR ERROR
    path("api/", include("analyzer.urls")),
]

if settings.DEBUG:

    urlpatterns += static(

        settings.MEDIA_URL,

        document_root=settings.MEDIA_ROOT
    )

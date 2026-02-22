from django.contrib import admin
from django.urls import include, path

from projects.views import custom_404, custom_500

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("projects.urls")),
]

handler404 = custom_404
handler500 = custom_500

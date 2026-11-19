from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.users.urls")),
    path("documents/", include("apps.documents.urls")),
    path("notes/", include("apps.notes.urls")),
]

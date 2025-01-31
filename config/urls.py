from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("orders.urls")),
]

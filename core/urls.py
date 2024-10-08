from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("register/", views.WorkOrderCreateView.as_view(), name="workorder_form"),
]

from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("ordem/novo/", views.WorkOrderCreateView.as_view(), name="workorder_form"),
]

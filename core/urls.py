from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("register/", views.WorkOrderFormView.as_view(), name="work-order-form"),
]

from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("ordens/", views.WorkOrderListView.as_view(), name="workorder_list"),
    path("ordens/novo/", views.WorkOrderCreateView.as_view(), name="workorder_form"),
]

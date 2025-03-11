from django.urls import path

from . import views

app_name = "api"

urlpatterns = [
    path("categories/", views.CategoryListView.as_view(), name="categories"),
    path("depts/", views.DepartmentListView.as_view(), name="depts"),
    path("workorders/create/", views.WorkOrderCreateAPIView.as_view(), name="workorder_create"),
]

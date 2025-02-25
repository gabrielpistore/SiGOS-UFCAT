from django.urls import path

from . import views

urlpatterns = [
    path("categories/", views.CategoryListView.as_view()),
    path("depts/", views.DepartmentListView.as_view()),
    path("workorders/create/", views.WorkOrderCreateAPIView.as_view()),
]

from django.urls import path

from control_panel import views

app_name = "control_panel"

# fmt: off
urlpatterns = [
    path("categorias", views.CategoryListView.as_view(), name="category_list"),
    path("categorias/<int:pk>/excluir", views.CategoryDeleteView.as_view(), name="category_delete"),
    path("categorias/novo", views.CategoryCreateView.as_view(), name="category_create"),
    path("departamentos", views.DepartmentListView.as_view(), name="department_list"),
    path("departamentos/<int:pk>/excluir", views.DepartmentDeleteView.as_view(), name="department_delete"),
    path("departamentos/novo", views.DepartmentCreateView.as_view(), name="department_create"),
    path("funcionarios", views.EmployeeListView.as_view(), name="employee_list"),
    path("funcionarios/<int:pk>/excluir", views.EmployeeDeleteView.as_view(), name="employee_delete"),
    path("funcionarios/novo", views.EmployeeCreateView.as_view(), name="employee_create"),
]

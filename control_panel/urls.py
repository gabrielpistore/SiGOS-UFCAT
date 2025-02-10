from django.urls import path

from control_panel import views

app_name = "control_panel"

# fmt: off
urlpatterns = [
    path("categorias/novo", views.CategoryCreateView.as_view(), name="category_create"),
]

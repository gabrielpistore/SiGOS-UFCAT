from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView

from orders.models import Category, Employee


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = "__all__"
    template_name = "control_panel/pages/category_create_form.html"
    success_url = "/painel-de-controle/categorias/novo"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Categoria criada com sucesso!")
        return response


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    fields = "__all__"
    template_name = "control_panel/pages/employee_create_form.html"
    success_url = "/painel-de-controle/funcionarios/novo"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Funcionário criado com sucesso!")
        return response

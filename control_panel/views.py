from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from orders.models import Category, Department, Employee


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "control_panel/pages/category_list.html"
    context_object_name = "categories"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        paginator = Paginator(self.object_list, self.paginate_by)
        page = request.GET.get("page", 1)

        try:
            categories = paginator.page(page)
        except Exception:
            categories = []

        context = {"categories": categories}

        # If it's an HTMX request, return only the category list
        if request.htmx:
            return render(
                request, "control_panel/partials/category_list_partial.html", context
            )

        return render(request, self.template_name, context)


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = "__all__"
    template_name = "control_panel/pages/category_create_form.html"
    success_url = reverse_lazy("control_panel:category_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Categoria criada com sucesso!")
        return response


class CategoryDeleteView(LoginRequiredMixin, View):
    def delete(self, request, pk, *args, **kwargs):
        category = get_object_or_404(Category, pk=pk)
        try:
            category.delete()
            messages.success(request, "Categoria excluída com sucesso!")
            return JsonResponse(
                {"message": "Category deleted successfully!"}, status=200
            )
        except Exception:
            messages.error(request, "Não foi possível excluir a categoria.")
            return JsonResponse({"message": "Failed to delete category."}, status=500)


class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = "control_panel/pages/dept_list.html"
    context_object_name = "departments"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        paginator = Paginator(self.object_list, self.paginate_by)
        page = request.GET.get("page", 1)

        try:
            departments = paginator.page(page)
        except Exception:
            departments = []

        context = {"departments": departments}

        # If it's an HTMX request, return only the department list
        if request.htmx:
            return render(
                request, "control_panel/partials/dept_list_partial.html", context
            )

        return render(request, self.template_name, context)


class DepartmentCreateView(LoginRequiredMixin, CreateView):
    model = Department
    fields = "__all__"
    template_name = "control_panel/pages/dept_create_form.html"
    success_url = reverse_lazy("control_panel:department_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Departamento criado com sucesso!")
        return response


class DepartmentDeleteView(LoginRequiredMixin, View):
    def delete(self, request, pk, *args, **kwargs):
        department = get_object_or_404(Department, pk=pk)
        try:
            department.delete()
            messages.success(request, "Departamento excluído com sucesso!")
            return JsonResponse(
                {"message": "Department deleted successfully!"}, status=200
            )
        except Exception:
            messages.error(request, "Não foi possível excluir o departamento.")
            return JsonResponse({"message": "Failed to delete department."}, status=500)


class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = "control_panel/pages/employee_list.html"
    context_object_name = "employees"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        paginator = Paginator(self.object_list, self.paginate_by)
        page = request.GET.get("page", 1)

        try:
            employees = paginator.page(page)
        except Exception:
            employees = []

        context = {"employees": employees}

        # If it's an HTMX request, return only the employee list
        if request.htmx:
            return render(
                request, "control_panel/partials/employee_list_partial.html", context
            )

        return render(request, self.template_name, context)


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    fields = "__all__"
    template_name = "control_panel/pages/employee_create_form.html"
    success_url = reverse_lazy("control_panel:employee_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Funcionário criado com sucesso!")
        return response


class EmployeeDeleteView(LoginRequiredMixin, View):
    def delete(self, request, pk, *args, **kwargs):
        employee = get_object_or_404(Employee, pk=pk)
        try:
            employee.delete()
            messages.success(request, "Funcionário excluído com sucesso!")
            return JsonResponse(
                {"message": "Employee deleted successfully!"}, status=200
            )
        except Exception as e:
            messages.error(request, "Não foi possível excluir o funcionário.")
            self.raise_exception(e)
            return JsonResponse({"message": "Failed to delete employee."}, status=500)

from django import forms
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from core.models import WorkOrder


class HomeView(ListView):
    model = WorkOrder
    template_name = "core/home.html"
    context_object_name = "work_orders"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("category", "responsible_employee")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["last_modified_orders"] = WorkOrder.objects.order_by("-created_at")[:6]
        return context


class WorkOrderCreateView(CreateView):
    model = WorkOrder
    fields = "__all__"
    success_url = "/"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["service_start_date"].widget = forms.DateInput(attrs={"type": "date"})
        form.fields["service_end_date"].widget = forms.DateInput(attrs={"type": "date"})
        form.fields["opening_date"].widget = forms.DateInput(attrs={"type": "date"})
        form.fields["closing_date"].widget = forms.DateInput(attrs={"type": "date"})
        return form

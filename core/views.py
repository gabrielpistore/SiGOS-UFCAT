from django import forms
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from core.models import WorkOrder


class HomeView(TemplateView):
    template_name = "core/home.html"


class WorkOrderCreateView(CreateView):
    model = WorkOrder
    fields = "__all__"
    success_url = "/"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["service_start_date"].widget = forms.DateInput(
            attrs={"type": "date"}
        )
        form.fields["service_end_date"].widget = forms.DateInput(attrs={"type": "date"})
        form.fields["opening_date"].widget = forms.DateInput(attrs={"type": "date"})
        form.fields["closing_date"].widget = forms.DateInput(attrs={"type": "date"})
        return form

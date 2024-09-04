from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from core.models import WorkOrder


class HomeView(TemplateView):
    template_name = "core/home.html"


class WorkOrderCreateView(CreateView):
    model = WorkOrder
    fields = "__all__"
    success_url = "/"

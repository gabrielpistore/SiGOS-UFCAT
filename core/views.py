from django.views.generic.base import TemplateView
# from django.views.generic.edit import FormView


class HomeView(TemplateView):
    template_name = "core/home.html"


class WorkOrderFormView(TemplateView):
    template_name = "core/work-order-form.html"

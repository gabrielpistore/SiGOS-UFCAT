from django import forms
from django.utils import timezone

from orders.models import Category, Department, Employee, WorkOrder


class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = [
            "requested_by",
            "dept_name",
            "email",
            "phone",
            "category",
            "responsible_employee",
            "impact",
            "urgency",
            "priority",
            "location",
            "opening_date",
            "closing_date",
            "service_start_date",
            "service_end_date",
            "status",
            "title",
            "report_description",
            "image",
        ]
        widgets = {
            "opening_date": forms.DateTimeInput(
                attrs={"type": "date"}, format="%Y-%m-%d"
            ),
            "closing_date": forms.DateTimeInput(
                attrs={"type": "date"}, format="%Y-%m-%d"
            ),
            "service_start_date": forms.DateTimeInput(
                attrs={"type": "date"}, format="%Y-%m-%d"
            ),
            "service_end_date": forms.DateTimeInput(
                attrs={"type": "date"}, format="%Y-%m-%d"
            ),
            "report_description": forms.Textarea(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Default values
        self.fields["opening_date"].initial = timezone.now().strftime("%Y-%m-%d")
        self.fields["impact"].initial = "Baixo"
        self.fields["urgency"].initial = "Baixo"
        self.fields["priority"].initial = "Baixo"
        self.fields["status"].initial = "Aberto"

        self.fields["dept_name"].queryset = Department.objects.all()
        self.fields["category"].queryset = Category.objects.all()
        self.fields["responsible_employee"].queryset = Employee.objects.all()

        # Add empty label to select fields
        for field_name in [
            "dept_name",
            "category",
            "responsible_employee",
            "impact",
            "urgency",
            "priority",
            "status",
        ]:
            self.fields[field_name].empty_label = "Selecione"

import json

from django.http import JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from orders.models import Category, Department, WorkOrder


@method_decorator(csrf_exempt, name="dispatch")
class WorkOrderCreateAPIView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            required_fields = [
                "requested_by",
                "dept_name",
                "phone",
                "category",
                "location",
                "title",
                "report_description",
            ]

            # Check if all required fields are present
            if not all(field in data for field in required_fields):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            # Get the related objects
            dept = Department.objects.get(name=data["dept_name"])
            cat = Category.objects.get(name=data["category"])

            # Create WorkOrder
            work_order = WorkOrder.objects.create(
                requested_by=data["requested_by"],
                dept_name=dept,
                phone=data["phone"],
                category=cat,
                location=data["location"],
                title=data["title"],
                report_description=data["report_description"],
                status="Aberto",
                opening_date=timezone.now(),
            )

            return JsonResponse(
                {"id": work_order.id, "message": "Work order created successfully"},
                status=201,
            )

        except Department.DoesNotExist:
            return JsonResponse({"error": "Department not found"}, status=404)
        except Category.DoesNotExist:
            return JsonResponse({"error": "Category not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)


class CategoryListAPIView(View):
    def get(self, request, *args, **kwargs):
        cats = Category.objects.values_list("name", flat=True)
        return JsonResponse(list(cats), safe=False)


class DeptListAPIView(View):
    def get(self, request, *args, **kwargs):
        depts = Department.objects.values_list("name", flat=True)
        return JsonResponse(list(depts), safe=False)

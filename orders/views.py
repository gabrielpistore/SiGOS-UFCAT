import json

from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from orders.forms import WorkOrderForm
from orders.models import Category, Department, WorkOrder


class HomeView(ListView):
    model = WorkOrder
    template_name = "orders/pages/home.html"
    context_object_name = "work_orders"

    def get_queryset(self):
        return (
            super().get_queryset().prefetch_related("category", "responsible_employee")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["last_modified_orders"] = WorkOrder.objects.order_by("-created_at")[:6]
        current_year = timezone.now().year
        context["orders_data"] = {
            "opened": WorkOrder.objects.filter(
                status="Aberto", created_at__year=current_year
            ).count(),
            "ongoing": WorkOrder.objects.filter(
                status="Em Andamento", created_at__year=current_year
            ).count(),
            "closed": WorkOrder.objects.filter(
                status="Fechado", created_at__year=current_year
            ).count(),
        }
        return context


class WorkOrderCreateView(CreateView):
    model = WorkOrder
    form_class = WorkOrderForm
    template_name = "orders/pages/workorder_create_form.html"
    success_url = "/"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Ordem de serviço criada com sucesso!")
        return response


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


class WorkOrderListView(ListView):
    model = WorkOrder
    template_name = "orders/pages/workorder_list.html"
    context_object_name = "work_orders"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class WorkOrderListViewJSONResponse(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))

        # Default to 'created_at' column
        order_column_index = int(request.GET.get("order[0][column]", 3))
        order_dir = request.GET.get("order[0][dir]", "desc")
        columns = ["id", "title", "category", "created_at", "status", "actions"]

        # Build ordering query
        sort_column = columns[order_column_index]
        if order_dir == "desc":
            sort_column = f"-{sort_column}"

        # Queryset with search filtering
        queryset = WorkOrder.objects.all().select_related("category")

        # Apply filters
        category = request.GET.get("category")
        if category:
            queryset = queryset.filter(category__name=category)

        id_filter = request.GET.get("id")
        if id_filter:
            queryset = queryset.filter(id=id_filter)

        status = request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)

        location = request.GET.get("location")
        if location:
            queryset = queryset.filter(location__icontains=location)

        # Date range filter for created_at
        start_created_at = request.GET.get("start_created_at")
        end_created_at = request.GET.get("end_created_at")

        if start_created_at:
            start_date = parse_date(start_created_at)
            if start_date:
                queryset = queryset.filter(created_at__gte=start_date)

        if end_created_at:
            end_date = parse_date(end_created_at)
            if end_date:
                queryset = queryset.filter(created_at__lte=end_date)

        # Apply sorting
        queryset = queryset.order_by(sort_column)

        # Pagination
        total_records = queryset.count()
        paginator = Paginator(queryset, length)
        current_page = (start // length) + 1
        page = paginator.get_page(current_page)

        # Prepare response data
        data = [
            {
                "id": work_order.id,
                "title": work_order.title,
                "status": work_order.status,
                "created_at": work_order.created_at.strftime("%d/%m/%Y"),
                "category": work_order.category.name if work_order.category else "",
                "actions": f"""
                    <div class="flex gap-2 text-primary">
                        <a href="{work_order.id}/editar/">
                            <i class="fa-solid fa-pen-to-square"></i>
                        </a>                        
                        <button data-work-order-id="{work_order.id}" class="delete-work-order">
                            <i class="fa-solid fa-trash"></i>
                        </button>
                    </div>
                """,
            }
            for work_order in page.object_list
        ]

        return JsonResponse(
            {
                "draw": draw,
                "recordsTotal": total_records,
                "recordsFiltered": total_records,
                "data": data,
            }
        )


class WorkOrderDeleteViewJSONResponse(View):
    def delete(self, request, pk, *args, **kwargs):
        try:
            work_order = WorkOrder.objects.get(pk=pk)
            work_order.delete()
            return JsonResponse({"success": True})
        except WorkOrder.DoesNotExist:
            return JsonResponse({"error": "Work order not found."}, status=404)


class WorkOrderUpdateView(UpdateView):
    model = WorkOrder
    form_class = WorkOrderForm
    template_name = "orders/pages/workorder_update_form.html"
    success_url = "/"


class CategoryListAPIView(View):
    def get(self, request, *args, **kwargs):
        cats = Category.objects.values_list("name", flat=True)
        return JsonResponse(list(cats), safe=False)


class DeptListAPIView(View):
    def get(self, request, *args, **kwargs):
        depts = Department.objects.values_list("name", flat=True)
        return JsonResponse(list(depts), safe=False)

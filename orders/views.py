from django import forms
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from orders.models import WorkOrder


class HomeView(ListView):
    model = WorkOrder
    template_name = "orders/index.html"
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
                        <a href="">
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


class WorkOrderListView(ListView):
    model = WorkOrder
    context_object_name = "work_orders"

    def get_queryset(self):
        return (
            super().get_queryset().prefetch_related("category", "responsible_employee")
        )


class WorkOrderDeleteView(View):
    def delete(self, request, pk, *args, **kwargs):
        try:
            work_order = WorkOrder.objects.get(pk=pk)
            work_order.delete()
            return JsonResponse({"success": True})
        except WorkOrder.DoesNotExist:
            return JsonResponse({"error": "Work order not found."}, status=404)

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date
from django.utils.timezone import now, timedelta
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from orders.forms import WorkOrderForm
from orders.models import Category, WorkOrder


class HomeView(LoginRequiredMixin, ListView):
    model = WorkOrder
    template_name = "orders/pages/home.html"
    context_object_name = "work_orders"

    def get_queryset(self):
        return (
            super().get_queryset().prefetch_related("category", "responsible_employee")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_year = now().year
        one_month_ago = now() - timedelta(days=30)

        context["orders"] = {
            "opened": WorkOrder.objects.filter(
                status="Aberto", created_at__year=current_year
            ).count(),
            "ongoing": WorkOrder.objects.filter(
                status="Em Andamento", created_at__year=current_year
            ).count(),
            "closed": WorkOrder.objects.filter(
                status="Fechado", created_at__year=current_year
            ).count(),
            "new_orders": WorkOrder.objects.filter(
                created_at__gte=one_month_ago
            ).count(),
            "high_priority_orders": WorkOrder.objects.filter(priority="Alto")
            .exclude(status="Fechado")
            .count(),
            "critical_priority_orders": WorkOrder.objects.filter(priority="Crítico")
            .exclude(status="Fechado")
            .count(),
            "low_medium_priority_orders": WorkOrder.objects.filter(
                priority__in=["Baixo", "Médio"]
            )
            .exclude(status="Fechado")
            .count(),
            "history": WorkOrder.history.all()[:6],
        }

        return context


class WorkOrderListViewJSONResponse(LoginRequiredMixin, View):
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

        queryset = WorkOrder.objects.all().select_related("category")

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

        queryset = queryset.order_by(sort_column)

        # Pagination
        total_records = queryset.count()
        paginator = Paginator(queryset, length)
        current_page = (start // length) + 1
        page = paginator.get_page(current_page)

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


class WorkOrderListView(LoginRequiredMixin, TemplateView):
    template_name = "orders/pages/workorder_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class WorkOrderCreateView(LoginRequiredMixin, CreateView):
    model = WorkOrder
    form_class = WorkOrderForm
    template_name = "orders/pages/workorder_create_form.html"
    success_url = "/"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Ordem de serviço criada com sucesso!")
        return response


class WorkOrderUpdateView(LoginRequiredMixin, UpdateView):
    model = WorkOrder
    form_class = WorkOrderForm
    template_name = "orders/pages/workorder_update_form.html"
    success_url = reverse_lazy("orders:workorder_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        # Explicitly set the history_user
        self.object.save()  # Ensure the object is saved first
        self.object.history.last().history_user = self.request.user
        self.object.history.last().save()
        messages.success(self.request, "Ordem de serviço atualizada com sucesso!")
        return response


class WorkOrderDeleteViewJSONResponse(LoginRequiredMixin, View):
    def delete(self, request, pk, *args, **kwargs):
        try:
            work_order = WorkOrder.objects.get(pk=pk)
            work_order.delete()
            return JsonResponse({"success": True})
        except WorkOrder.DoesNotExist:
            return JsonResponse({"error": "Work order not found."}, status=404)


class WorkOrderHistoryListViewJSONResponse(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        order_column_index = int(request.GET.get("order[0][column]", 5))
        order_dir = request.GET.get("order[0][dir]", "desc")

        columns = [
            "id",
            "title",
            "history_user",
            "status",
            "changes",
            "history_date",
        ]

        sort_column = columns[order_column_index]
        if order_dir == "desc":
            sort_column = f"-{sort_column}"

        queryset = (
            WorkOrder.history.all().select_related("history_user").order_by(sort_column)
        )

        # pagination
        total_records = queryset.count()
        paginated_queryset = queryset[start : start + length]

        data = []
        for record in paginated_queryset:
            len(paginated_queryset)
            if record.history_type == "+":
                change_message = "Ordem criada"
            elif record.history_type == "-":
                change_message = "Ordem deletada"
            else:
                change_message = "Ordem atualizada"

            data.append(
                {
                    "id": record.id,
                    "title": record.title,
                    "history_user": str(record.history_user)
                    if record.history_user
                    else None,
                    "changes": change_message,
                    "status": record.status,
                    "history_date": record.history_date.isoformat(),
                }
            )

        return JsonResponse(
            {
                "draw": draw,
                "recordsTotal": total_records,
                "recordsFiltered": total_records,
                "data": data,
            }
        )


class WorkOrderHistoryListView(LoginRequiredMixin, TemplateView):
    template_name = "orders/pages/history.html"

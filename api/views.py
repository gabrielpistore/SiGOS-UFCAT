from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny

from api.serializers import (
    CategorySerializer,
    DepartmentSerializer,
    WorkOrderCreateSerializer,
)
from orders.models import Category, Department, WorkOrder


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DepartmentListView(ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class WorkOrderCreateAPIView(CreateAPIView):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderCreateSerializer
    permission_classes = [AllowAny]

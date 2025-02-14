from rest_framework.generics import ListAPIView

from api.serializers import CategorySerializer, DepartmentSerializer
from orders.models import Category, Department


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DepartmentListView(ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

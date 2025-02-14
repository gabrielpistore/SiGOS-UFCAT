from django.utils import timezone
from rest_framework import serializers

from orders.models import Category, Department, WorkOrder


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class WorkOrderCreateSerializer(serializers.ModelSerializer):
    dept_name = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        write_only=True,
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True,
    )
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = WorkOrder
        fields = [
            "requested_by",
            "dept_name",
            "phone",
            "category",
            "location",
            "title",
            "report_description",
            "image",
        ]

    def create(self, validated_data):
        # Set the status to "Aberto" (Open) by default
        validated_data["status"] = "Aberto"
        validated_data["opening_date"] = timezone.now()
        return super().create(validated_data)

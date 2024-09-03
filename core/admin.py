from django.contrib import admin

from core.models import Category, Employee, WorkOrder


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    pass

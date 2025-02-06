from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from orders.models import Category, Department, Employee, WorkOrder


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass


@admin.register(WorkOrder)
class WorkOrderAdmin(SimpleHistoryAdmin):
    pass

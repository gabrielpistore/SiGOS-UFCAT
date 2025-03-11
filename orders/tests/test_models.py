import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from pytest import raises

from orders.models import WorkOrderProgress


@pytest.mark.django_db
class TestCategoryModel:
    def test_category_creation(self, category):
        assert category.name == "Test Category"
        assert str(category) == "Test Category"


@pytest.mark.django_db
class TestDepartmentModel:
    def test_department_creation(self, department):
        assert department.name == "Test Department"
        assert str(department) == "Test Department"


@pytest.mark.django_db
class TestEmployeeModel:
    def test_employee_creation(self, employee):
        assert employee.name == "Test Employee"
        assert employee.email == "employee@example.com"
        assert employee.mobile_phone == "1234567890"
        assert str(employee) == "Test Employee"


@pytest.mark.django_db
class TestWorkOrderModel:
    def test_work_order_creation(self, work_order):
        assert work_order.requested_by == "Test Requester"
        assert work_order.email == "requester@example.com"
        assert work_order.status == "Aberto"
        assert work_order.title == "Test Work Order"
        assert str(work_order) == "Test Work Order"

    def test_work_order_auto_close_date(self, work_order):
        # Initially closing_date should be None
        assert work_order.closing_date is None

        # Update status to "Fechado"
        work_order.status = "Fechado"
        work_order.save()

        # closing_date should be set automatically
        assert work_order.closing_date is not None

    def test_work_order_validation_closing_date(self, work_order):
        # Set closing_date before opening_date
        work_order.opening_date = timezone.now()
        work_order.closing_date = timezone.now() - timezone.timedelta(days=1)

        with raises(ValidationError) as excinfo:
            work_order.full_clean()

        assert "closing_date" in str(excinfo.value)

    def test_work_order_validation_service_dates(self, work_order):
        # Set service_end_date before service_start_date
        work_order.service_start_date = timezone.now()
        work_order.service_end_date = timezone.now() - timezone.timedelta(hours=1)

        with raises(ValidationError) as excinfo:
            work_order.full_clean()

        assert "service_end_date" in str(excinfo.value)

    def test_work_order_status_closed_without_service_end_date(self, work_order):
        # Set status to "Fechado" with service_start_date but without service_end_date
        work_order.status = "Fechado"
        work_order.service_start_date = timezone.now()
        work_order.service_end_date = None

        with raises(ValidationError) as excinfo:
            work_order.full_clean()

        assert "service_end_date" in str(excinfo.value)


@pytest.mark.django_db
class TestWorkOrderProgressModel:
    def test_work_order_progress_creation(self, work_order):
        progress = WorkOrderProgress.objects.create(
            work_order=work_order, progress_description="Test progress description"
        )

        assert progress.work_order == work_order
        assert progress.progress_description == "Test progress description"
        assert str(progress) == "Test progress description"

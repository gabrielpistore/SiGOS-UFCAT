import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from rest_framework.test import APIClient

from orders.models import Category, Department, Employee, WorkOrder


@pytest.fixture
def user():
    User = get_user_model()
    user = User.objects.create_user(
        username="testuser", email="test@example.com", password="testpassword123"
    )
    return user


@pytest.fixture
def admin_user():
    User = get_user_model()
    user = User.objects.create_superuser(
        username="admin", email="admin@example.com", password="adminpassword123"
    )
    return user


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def authenticated_client(client, user):
    client.force_login(user)
    return client


@pytest.fixture
def admin_client(client, admin_user):
    client.force_login(admin_user)
    return client


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_api_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def category():
    return Category.objects.create(name="Test Category")


@pytest.fixture
def department():
    return Department.objects.create(name="Test Department")


@pytest.fixture
def employee():
    return Employee.objects.create(
        name="Test Employee", email="employee@example.com", mobile_phone="1234567890"
    )


@pytest.fixture
def work_order(category, department):
    return WorkOrder.objects.create(
        requested_by="Test Requester",
        dept_name=department,
        email="requester@example.com",
        phone="9876543210",
        category=category,
        location="Test Location",
        status="Aberto",
        title="Test Work Order",
        report_description="This is a test work order.",
    )

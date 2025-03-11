import json

import pytest
from django.urls import reverse

from orders.models import Category, Department, Employee


@pytest.mark.django_db
class TestCategoryViews:
    def test_category_list_view_authenticated(self, authenticated_client, category):
        url = reverse("control_panel:category_list")
        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert "categories" in response.context
        assert category in response.context["categories"]

    def test_category_list_view_unauthenticated(self, client):
        url = reverse("control_panel:category_list")
        response = client.get(url)

        # Should redirect to login page
        assert response.status_code == 302
        assert "login" in response.url

    def test_category_create_view_get(self, authenticated_client):
        url = reverse("control_panel:category_create")
        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert "form" in response.context

    def test_category_create_view_post(self, authenticated_client):
        url = reverse("control_panel:category_create")
        data = {"name": "New Test Category"}
        response = authenticated_client.post(url, data)

        assert response.status_code == 302  # Redirect after successful creation
        assert Category.objects.filter(name="New Test Category").exists()

    def test_category_delete_view(self, authenticated_client, category):
        url = reverse("control_panel:category_delete", kwargs={"pk": category.id})
        response = authenticated_client.delete(
            url, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        assert response.status_code == 200
        data = json.loads(response.content)
        assert "message" in data
        assert not Category.objects.filter(id=category.id).exists()


@pytest.mark.django_db
class TestDepartmentViews:
    def test_department_list_view_authenticated(self, authenticated_client, department):
        url = reverse("control_panel:department_list")
        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert "departments" in response.context
        assert department in response.context["departments"]

    def test_department_create_view_get(self, authenticated_client):
        url = reverse("control_panel:department_create")
        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert "form" in response.context

    def test_department_create_view_post(self, authenticated_client):
        url = reverse("control_panel:department_create")
        data = {"name": "New Test Department"}
        response = authenticated_client.post(url, data)

        assert response.status_code == 302  # Redirect after successful creation
        assert Department.objects.filter(name="New Test Department").exists()

    def test_department_delete_view(self, authenticated_client, department):
        url = reverse("control_panel:department_delete", kwargs={"pk": department.id})
        response = authenticated_client.delete(
            url, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        assert response.status_code == 200
        data = json.loads(response.content)
        assert "message" in data
        assert not Department.objects.filter(id=department.id).exists()


@pytest.mark.django_db
class TestEmployeeViews:
    def test_employee_list_view_authenticated(self, authenticated_client, employee):
        url = reverse("control_panel:employee_list")
        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert "employees" in response.context
        assert employee in response.context["employees"]

    def test_employee_create_view_get(self, authenticated_client):
        url = reverse("control_panel:employee_create")
        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert "form" in response.context

    def test_employee_create_view_post(self, authenticated_client):
        url = reverse("control_panel:employee_create")
        data = {
            "name": "New Test Employee",
            "email": "newemployee@example.com",
            "mobile_phone": "5555555555",
        }
        response = authenticated_client.post(url, data)

        assert response.status_code == 302  # Redirect after successful creation
        assert Employee.objects.filter(name="New Test Employee").exists()

    def test_employee_delete_view(self, authenticated_client, employee):
        url = reverse("control_panel:employee_delete", kwargs={"pk": employee.id})
        response = authenticated_client.delete(
            url, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        assert response.status_code == 200
        data = json.loads(response.content)
        assert "message" in data
        assert not Employee.objects.filter(id=employee.id).exists()

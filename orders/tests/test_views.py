import json

import pytest
from django.urls import reverse

from orders.models import WorkOrder, WorkOrderProgress


@pytest.mark.django_db
class TestHomeView:
    def test_home_view_authenticated(self, authenticated_client):
        url = reverse("orders:home")
        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert "work_orders" in response.context
        assert "orders" in response.context

    def test_home_view_unauthenticated(self, client):
        url = reverse("orders:home")
        response = client.get(url)

        # Should redirect to login page
        assert response.status_code == 302
        assert "login" in response.url


@pytest.mark.django_db
class TestWorkOrderListView:
    def test_workorder_list_view_authenticated(self, authenticated_client):
        url = reverse("orders:workorder_list")
        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert "categories" in response.context

    def test_workorder_list_view_unauthenticated(self, client):
        url = reverse("orders:workorder_list")
        response = client.get(url)

        # Should redirect to login page
        assert response.status_code == 302
        assert "login" in response.url


@pytest.mark.django_db
class TestWorkOrderListViewJSONResponse:
    def test_workorder_list_json_authenticated(self, authenticated_client, work_order):
        url = reverse("orders:workorder_list_json")
        response = authenticated_client.get(url, {"draw": 1, "start": 0, "length": 10})

        assert response.status_code == 200
        data = json.loads(response.content)
        assert "data" in data
        assert len(data["data"]) >= 1
        assert data["data"][0]["id"] == work_order.id
        assert data["data"][0]["title"] == work_order.title

    def test_workorder_list_json_filter_category(
        self, authenticated_client, work_order, category
    ):
        url = reverse("orders:workorder_list_json")
        response = authenticated_client.get(
            url, {"draw": 1, "start": 0, "length": 10, "category": category.name}
        )

        assert response.status_code == 200
        data = json.loads(response.content)
        assert len(data["data"]) == 1


@pytest.mark.django_db
class TestWorkOrderDetailView:
    def test_workorder_detail_view_authenticated(
        self, authenticated_client, work_order
    ):
        url = reverse("orders:workorder_detail", kwargs={"pk": work_order.id})
        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert response.context["work_order"] == work_order


@pytest.mark.django_db
class TestWorkOrderCreateView:
    def test_workorder_create_view_get(self, authenticated_client):
        url = reverse("orders:workorder_create")
        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert "form" in response.context

    def test_workorder_create_view_post(
        self, authenticated_client, category, department
    ):
        url = reverse("orders:workorder_create")
        data = {
            "requested_by": "New Requester",
            "dept_name": department.id,
            "email": "new@example.com",
            "phone": "5555555555",
            "category": category.id,
            "location": "New Location",
            "status": "Aberto",
            "title": "New Work Order",
            "report_description": "This is a new work order.",
            "impact": "Baixo",
            "urgency": "Baixo",
            "priority": "Baixo",
        }
        response = authenticated_client.post(url, data)

        assert response.status_code == 302  # Redirect after successful creation
        assert WorkOrder.objects.filter(title="New Work Order").exists()


@pytest.mark.django_db
class TestWorkOrderUpdateView:
    def test_workorder_update_view_get(self, authenticated_client, work_order):
        url = reverse("orders:workorder_update", kwargs={"pk": work_order.id})
        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert "form" in response.context

    def test_workorder_update_view_post(self, authenticated_client, work_order):
        url = reverse("orders:workorder_update", kwargs={"pk": work_order.id})
        data = {
            "requested_by": work_order.requested_by,
            "dept_name": work_order.dept_name.id,
            "email": work_order.email,
            "phone": work_order.phone,
            "category": work_order.category.id,
            "location": "Updated Location",
            "status": "Em Andamento",
            "title": "Updated Work Order",
            "report_description": work_order.report_description,
            "impact": "Médio",
            "urgency": "Médio",
            "priority": "Médio",
            "progress": "Progress update for testing",
        }
        response = authenticated_client.post(url, data)

        assert response.status_code == 302  # Redirect after successful update

        # Check that the work order was updated
        updated_work_order = WorkOrder.objects.get(id=work_order.id)
        assert updated_work_order.location == "Updated Location"
        assert updated_work_order.status == "Em Andamento"
        assert updated_work_order.title == "Updated Work Order"

        # Check that progress was added
        assert WorkOrderProgress.objects.filter(
            work_order=work_order, progress_description="Progress update for testing"
        ).exists()


@pytest.mark.django_db
class TestWorkOrderDeleteView:
    def test_workorder_delete(self, authenticated_client, work_order):
        url = reverse("orders:workorder_delete", kwargs={"pk": work_order.id})
        response = authenticated_client.delete(
            url, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )

        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["success"] is True
        assert not WorkOrder.objects.filter(id=work_order.id).exists()


@pytest.mark.django_db
class TestWorkOrderHistoryView:
    def test_workorder_history_list_view(self, authenticated_client):
        url = reverse("orders:history")
        response = authenticated_client.get(url)

        assert response.status_code == 200

    def test_workorder_history_json(self, authenticated_client, work_order):
        # Create history records by modifying work order
        work_order.title = "Updated Title"
        work_order.save()

        url = reverse("orders:history_json")
        response = authenticated_client.get(url, {"draw": 1, "start": 0, "length": 10})

        assert response.status_code == 200
        data = json.loads(response.content)
        assert "data" in data
        assert len(data["data"]) >= 1

import json
import tempfile

import pytest
from django.urls import reverse
from PIL import Image

from orders.models import WorkOrder


@pytest.mark.django_db
class TestCategoryListAPIView:
    def test_category_list_api(self, api_client, category):
        url = reverse("api:categories")
        response = api_client.get(url)

        assert response.status_code == 200
        data = json.loads(response.content)
        assert len(data) >= 1
        assert data[0]["name"] == category.name


@pytest.mark.django_db
class TestDepartmentListAPIView:
    def test_department_list_api(self, api_client, department):
        url = reverse("api:depts")
        response = api_client.get(url)

        assert response.status_code == 200
        data = json.loads(response.content)
        assert len(data) >= 1
        assert data[0]["name"] == department.name


@pytest.mark.django_db
class TestWorkOrderCreateAPIView:
    def test_work_order_create_api(self, api_client, category, department):
        url = reverse("api:workorder_create")

        # Create a temporary image file
        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_image:
            image = Image.new("RGB", (100, 100))
            image.save(temp_image, "JPEG")
            temp_image.seek(0)

            data = {
                "requested_by": "API Requester",
                "dept_name": department.id,
                "email": "api@example.com",
                "phone": "1234567890",
                "category": category.id,
                "location": "API Location",
                "title": "API Work Order",
                "report_description": "This is a work order created via API",
            }

            # Testing without image first
            response = api_client.post(url, data, format="multipart")

            assert response.status_code == 201
            assert WorkOrder.objects.filter(title="API Work Order").exists()
            work_order = WorkOrder.objects.get(title="API Work Order")
            assert work_order.status == "Aberto"  # Default status

            # Testing with image
            data["title"] = "API Work Order With Image"
            data["image"] = temp_image
            response = api_client.post(url, data, format="multipart")

            assert response.status_code == 201
            assert WorkOrder.objects.filter(title="API Work Order With Image").exists()
            work_order = WorkOrder.objects.get(title="API Work Order With Image")
            assert work_order.image  # Image should be uploaded

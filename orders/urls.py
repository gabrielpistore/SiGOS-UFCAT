from django.urls import path

from orders import views

app_name = "orders"

# fmt: off
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("ordens/", views.WorkOrderListView.as_view(), name="workorder_list"),
    path("ordens/novo/", views.WorkOrderCreateView.as_view(), name="workorder_form"),
    path("ordens/<int:pk>/deletar/", views.WorkOrderDeleteViewJSONResponse.as_view(), name="workorder_delete"),
    path("ordens/<int:pk>/editar/", views.WorkOrderUpdateView.as_view(), name="workorder_update"),
    path("api/ordens/", views.WorkOrderListViewJSONResponse.as_view(), name="workorder_list_json"),
]

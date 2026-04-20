from django.urls import path

from .views import (
    customer_create_view,
    customer_detail_view,
    customer_list_view,
    customer_lock_view,
    dashboard_view,
    order_detail_view,
    order_list_view,
    permission_list_view,
    product_create_view,
    product_delete_view,
    product_edit_view,
    product_list_view,
    report_view,
)

app_name = "dashboard"

urlpatterns = [
    path("", dashboard_view, name="dashboard"),
    path("reports/", report_view, name="reports"),
    path("orders/", order_list_view, name="orders"),
    path("orders/<str:order_id>/", order_detail_view, name="order_detail"),
    path("products/", product_list_view, name="products"),
    path("products/create/", product_create_view, name="product_create"),
    path("products/edit/<int:product_id>/", product_edit_view, name="product_edit"),
    path("products/delete/<int:product_id>/", product_delete_view, name="product_delete"),
    path("customers/", customer_list_view, name="customers"),
    path("customers/create/", customer_create_view, name="customer_create"),
    path("customers/<int:customer_id>/", customer_detail_view, name="customer_detail"),
    path("customers/<int:customer_id>/lock/", customer_lock_view, name="customer_lock"),
    path("permissions/", permission_list_view, name="permissions"),
]
from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    # HOME
    path("", views.home, name="home"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),

    # DASHBOARD
    path("dashboard/", views.dashboard_view, name="dashboard"),

    # ORDERS (ADMIN)
    path("dashboard/orders/", views.dashboard_orders_view, name="orders"),
    path("dashboard/orders/<int:pk>/", views.order_detail_view, name="order_detail"),

    # PRODUCTS (ADMIN)
    path("dashboard/products/", views.dashboard_products_view, name="products"),
    path("dashboard/products/create/", views.product_create, name="product_create"),
    path("dashboard/products/<int:pk>/edit/", views.product_edit, name="product_edit"),
    path("dashboard/products/<int:pk>/delete/", views.product_delete, name="product_delete"),

    # REPORTS
    path("dashboard/reports/", views.report_view, name="reports"),
]
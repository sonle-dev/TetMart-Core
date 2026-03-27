from django.urls import path
from . import views

urlpatterns = [

    # PRODUCTS (ADMIN)
    path('', views.dashboard_products_view, name='dashboard_products'),
    path("create/", views.product_create, name="product_create"),
    path("<int:pk>/edit/", views.product_edit, name="product_edit"),
    path("<int:pk>/delete/", views.product_delete, name="product_delete"),


]
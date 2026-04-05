from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('products/', views.dashboard_products, name='dashboard_products'),
    path('orders/', views.dashboard_orders_view, name='dashboard_orders'),
    path('order/<int:pk>/', views.order_detail_view, name='order_detail'),
    path('customers/', views.dashboard_customers, name='dashboard_customers'),
    path('report/', views.report_view, name='report'),
    path('permissions/', views.dashboard_permissions, name='permissions'),
]
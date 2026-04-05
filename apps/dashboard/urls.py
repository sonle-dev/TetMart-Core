from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard'),
    path('products/', views.dashboard_products, name='dashboard_products'),
    path('orders/', views.dashboard_orders, name='dashboard_orders'),
    path('customers/', views.dashboard_customers, name='dashboard_customers'),
    
    path('reports/', views.dashboard_reports, name='reports'),
    path('permissions/', views.dashboard_permissions, name='permissions'),
]
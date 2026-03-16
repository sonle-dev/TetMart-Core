from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('products/', views.dashboard_products, name='dashboard_products'),
    path('orders/', views.dashboard_orders, name='dashboard_orders'),
]
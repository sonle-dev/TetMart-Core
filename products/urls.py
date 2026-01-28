from django.urls import path
from . import views

urlpatterns = [
   

    path('', views.dashboard_products_view, name='product_list'),

    
    path('create/', views.product_create, name='product_create'),
    path('edit/<int:pk>/', views.product_edit, name='product_edit'),

    path('delete/<int:pk>/', views.product_delete, name='product_delete'),
]
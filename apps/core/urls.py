from django.urls import path

from .views import (
    index, 
    product_detail, 
    login_view, 
    register_view, 
    logout_view
)

from apps.dashboard.views import (
    dashboard_view, 
    report_view, 
    order_list_view, 
    order_detail_view,
    product_list_view,
    product_create_view,
    product_update_view,
    product_delete_view,
)

app_name = 'core'

urlpatterns = [
    # === PUBLIC URLS (Khách hàng) ===
    path('', index, name='home'),
    path('product-detail/<int:product_id>/', product_detail, name='product_detail'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    
    # === DASHBOARD URLS (Quản trị) ===
    path('dashboard/', dashboard_view, name='dashboard'),
    path('dashboard/reports/', report_view, name='reports'),
    path('dashboard/orders/', order_list_view, name='orders'),
    path('dashboard/orders/<int:pk>/', order_detail_view, name='order_detail'),

    # === PRODUCTS (Dashboard) ===
    path('dashboard/products/', product_list_view, name='products'),
    path('dashboard/products/create/', product_create_view, name='product_create'),
    path('dashboard/products/<int:pk>/update/', product_update_view, name='product_update'),
    path('dashboard/products/<int:pk>/delete/', product_delete_view, name='product_delete'),

    # URL phụ nếu bạn muốn mở bằng /dashboard/product_list/
    path('dashboard/product_list/', product_list_view, name='dashboard_product_list'),
]
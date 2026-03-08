from django.urls import path

# ---------------------------------------------------------
# 1. NHÓM VIEW CÔNG KHAI (Dành cho khách mua hàng)
# Lấy từ file: apps/core/views.py (ký hiệu là .views)
# ---------------------------------------------------------
from .views import (
    index, 
    product_detail, 
    login_view, 
    register_view, 
    logout_view
)

# ---------------------------------------------------------
# 2. NHÓM VIEW QUẢN TRỊ (Dành cho Admin)
# Lấy từ file: apps/dashboard/views.py
# ---------------------------------------------------------
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
    # Trang chủ Dashboard
    path('dashboard/', dashboard_view, name='dashboard'),
    
    # Báo cáo thống kê
    path('dashboard/reports/', report_view, name='reports'),
    
    # Quản lý đơn hàng (Danh sách)
    path('dashboard/orders/', order_list_view, name='orders'),
    
    # Chi tiết đơn hàng (Xem & Sửa)
    path('dashboard/orders/<int:pk>/', order_detail_view, name='order_detail'),

    # === PRODUCTS (Dashboard) ===
    path('dashboard/products/', product_list_view, name='product_list'),
    path('dashboard/products/create/', product_create_view, name='product_create'),
    path('dashboard/products/<int:pk>/update/', product_update_view, name='product_update'),
    path('dashboard/products/<int:pk>/delete/', product_delete_view, name='product_delete'),
]
from django.contrib import admin
from django.urls import path, include  
from django.conf import settings
from django.conf.urls.static import static

from products import views as product_views 
from products.views import home, product_detail
# report_view, buy_now_view import tạm thời, nếu chưa có thì cẩn thận lỗi
# from users.views import report_view 
from orders.views import buy_now_view 

urlpatterns = [
    # --- Trang Django Admin ---
    path('admin/', admin.site.urls),

    # --- Trang chủ và Chi tiết sản phẩm (Public) ---
    path('', home, name='home'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),

    # --- Xác thực (Login/Register) ---
    path('auth/', include('users.urls')),

    # --- Dashboard Tổng quan ---
    path('dashboard/', product_views.dashboard_view, name='dashboard'),
    
    # --- Dashboard Đơn hàng ---
    path('dashboard/order/<int:pk>/', product_views.order_detail_view, name='order_detail'),
    path('dashboard/orders/', product_views.dashboard_orders_view, name='dashboard_orders'),
    
    # --- Dashboard Báo cáo ---
    path('dashboard/report/', product_views.report_view, name='report'),

    
    path('dashboard/products/', include('products.urls')), 
    
    # --- Mua ngay ---
    path('buy-now/<int:product_id>/', buy_now_view, name='buy_now'),

    #Danh sach san pham
    path('products/', product_views.product_list_view, name='product_list'),

    path('cart/', include('apps.cart.urls')),
    path('orders/', include('apps.orders.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
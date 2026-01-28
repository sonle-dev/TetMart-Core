from django.contrib import admin
from django.urls import path, include  # ✅ Đã có include
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
    path('product/<int:pk>/', product_detail, name='product_detail'),

    # --- Xác thực (Login/Register) ---
    path('auth/', include('users.urls')),

    # --- Dashboard Tổng quan ---
    path('dashboard/', product_views.dashboard_view, name='dashboard'),
    
    # --- Dashboard Đơn hàng ---
    path('dashboard/order/<int:pk>/', product_views.order_detail_view, name='order_detail'),
    path('dashboard/orders/', product_views.dashboard_orders_view, name='dashboard_orders'),
    
    # --- Dashboard Báo cáo ---
    # (Lưu ý: Bạn đang import report_view từ product_views, check kỹ lại xem nó nằm ở đâu nhé)
    path('dashboard/report/', product_views.report_view, name='report'),

    # 👇👇👇 SỬA QUAN TRỌNG Ở ĐÂY 👇👇👇
    # Thay vì trỏ trực tiếp view, ta dùng include để nối sang file products/urls.py
    # Lúc này nó sẽ có cả trang danh sách (path '') và trang tạo mới (path 'create/')
    path('dashboard/products/', include('products.urls')), 
    
    # --- Mua ngay ---
    path('buy-now/<int:product_id>/', buy_now_view, name='buy_now'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
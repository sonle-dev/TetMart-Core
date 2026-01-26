from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products import views as product_views

from products.views import home, product_detail
from users.views import dashboard_view, order_detail_view, order_list_view, report_view

from orders.views import buy_now_view 

urlpatterns = [
    #  Trang quản trị Django
    path('admin/', admin.site.urls),

    #  Trang chủ  và Sản phẩm
    path('', home, name='home'),
    path('product/<int:pk>/', product_detail, name='product_detail'),

    #  Xác thực (Login/Register/Logout)
    path('auth/', include('users.urls')),

    #  Dashboard 
    path('dashboard/', dashboard_view, name='dashboard'),
    path('dashboard/order/<int:pk>/', order_detail_view, name='order_detail'),
    path('dashboard/orders/', order_list_view, name='order_list'),
    path('dashboard/reports/', report_view, name='reports'),
    path('dashboard/orders/', product_views.dashboard_orders_view, name='dashboard_orders'),
    path('dashboard/products/', product_views.dashboard_products_view, name='dashboard_products'),
     
    path('buy-now/<int:product_id>/', buy_now_view, name='buy_now'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
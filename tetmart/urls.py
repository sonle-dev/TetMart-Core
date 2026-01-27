from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



from products import views as product_views 
from products.views import home, product_detail
from users.views import report_view 

from orders.views import buy_now_view 

urlpatterns = [
    #  Trang Django
    path('admin/', admin.site.urls),

    #  Trang chu va san pham
    path('', home, name='home'),
    path('product/<int:pk>/', product_detail, name='product_detail'),

    #  xac thuc quyen
    path('auth/', include('users.urls')),
    path('dashboard/', product_views.dashboard_view, name='dashboard'),
    
    # cap nhat trang thai
    path('dashboard/order/<int:pk>/', product_views.order_detail_view, name='order_detail'),
    
    # danh sach don hang
    path('dashboard/orders/', product_views.dashboard_orders_view, name='dashboard_orders'),
    
    # danh sach san pham
    path('dashboard/products/', product_views.dashboard_products_view, name='dashboard_products'),
    path('dashboard/report/', product_views.report_view, name='report'),
    path('buy-now/<int:product_id>/', buy_now_view, name='buy_now'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
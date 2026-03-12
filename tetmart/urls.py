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

    # Core routes: home, product_detail, dashboard, reports, orders, products...
    path('', include(('apps.core.urls', 'core'), namespace='core')),

    # Auth
    path('auth/', include('users.urls')),

    # Buy now
    path('buy-now/<int:product_id>/', buy_now_view, name='buy_now'),

    # Cart
    path('cart/', include(('apps.cart.urls', 'cart'), namespace='cart')),
]

if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
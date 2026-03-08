from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from orders.views import buy_now_view

urlpatterns = [
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
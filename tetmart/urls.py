from django.contrib import admin
<<<<<<< HEAD
from django.urls import path, include  
=======
from django.urls import path, include
>>>>>>> develop
from django.conf import settings
from django.conf.urls.static import static

from products import views as product_views
from products.views import home, product_detail
from orders.views import buy_now_view
from apps.dashboard import views as dashboard_views
from orders import views as order_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),

    path('auth/', include('users.urls')),

    # Dashboard dùng view có phân quyền trong products/views.py
    path('dashboard/', product_views.dashboard_view, name='dashboard'),
    path('dashboard/orders/', product_views.dashboard_orders_view, name='dashboard_orders'),
    path('dashboard/order/<int:pk>/', product_views.order_detail_view, name='order_detail'),
    path('dashboard/report/', product_views.report_view, name='report'),

    # Products: dùng products.urls vì trong đó có create/edit/delete
    path('dashboard/products/', include('products.urls')),

    # Customers vẫn đang nằm ở apps/dashboard/views.py
    path('dashboard/customers/', dashboard_views.dashboard_customers, name='dashboard_customers'),
    path('dashboard/customers/create/', dashboard_views.customer_create, name='customer_create'),
    path('dashboard/customers/<int:pk>/', dashboard_views.customer_detail, name='customer_detail'),
    path('dashboard/customers/<int:pk>/lock/', dashboard_views.customer_lock, name='customer_lock'),

    # Permissions
    path('dashboard/permissions/', dashboard_views.dashboard_permissions, name='permissions'),
    path('dashboard/permissions/add-member/', dashboard_views.add_role_member, name='add_role_member'),
    path('dashboard/permissions/remove-member/', dashboard_views.remove_role_member, name='remove_role_member'),
    path('dashboard/permissions/update-permission/', dashboard_views.update_role_permission, name='update_role_permission'),

    path('buy-now/<int:product_id>/', buy_now_view, name='buy_now'),
    path('products/', product_views.product_list_view, name='product_list'),

    path('cart/', include('apps.cart.urls')),
<<<<<<< HEAD
    path('orders/', include('apps.orders.urls')),
=======
    path('orders/<int:order_id>/cancel/', order_views.cancel_order, name='cancel_order'),
    path('orders/<int:order_id>/reorder/', order_views.reorder_order, name='reorder_order'),
    path('orders/', include('orders.urls')),

    
>>>>>>> develop
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
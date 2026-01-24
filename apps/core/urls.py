from django.urls import path
from .views import index, product_detail, login_view, register_view, logout_view

app_name = 'core'

urlpatterns = [
    path('', index, name='home'), # Đường dẫn trống '' nghĩa là trang chủ
   path('product-detail/<int:product_id>/', product_detail, name='product_detail'), #trang chi tiet san pham
   path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]


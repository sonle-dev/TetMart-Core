from django.urls import path
from .views import index, product_detail

app_name = 'core'

urlpatterns = [
    path('', index, name='home'), # Đường dẫn trống '' nghĩa là trang chủ
   path('product-detail/<int:product_id>/', product_detail, name='product_detail'), #trang chi tiet san pham
]


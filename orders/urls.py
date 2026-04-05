from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('buy-now/<int:product_id>/', views.buy_now_view, name='buy_now'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('place-order/', views.place_order_view, name='place_order'),
    
]
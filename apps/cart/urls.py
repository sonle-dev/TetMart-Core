from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='detail'),
    path('add/<int:product_id>/', views.add, name='add'),
    path('update/<str:item_id>/', views.update, name='update'),
    path('remove/<str:item_id>/', views.remove, name='remove'),
    path('clear/', views.clear, name='clear'),
    path('add/<int:product_id>/', views.add, name='add'),
    path("buy-now/<int:product_id>/", views.buy_now, name="buy_now"),
]
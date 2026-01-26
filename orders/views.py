from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product 
from .models import Order

# xu li mua ngay
@login_required(login_url='login')
def buy_now_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
# Tao don moi
    Order.objects.create(
        user=request.user,
        total_price=product.price, 
        status='pending'
    )
    
    messages.success(request, f"Đã đặt mua thành công: {product.name}!")
    return redirect('home')

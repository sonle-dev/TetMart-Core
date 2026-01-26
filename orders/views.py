from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product 
# 👇 Quan trọng: Phải import thêm OrderItem
from .models import Order, OrderItem 

# xu li mua ngay
@login_required(login_url='login')
def buy_now_view(request, product_id):
    #  Lấy thông tin sản phẩm
    product = get_object_or_404(Product, id=product_id)
    
    #  Tạo đơn hàng tổng 
    order = Order.objects.create(
        user=request.user,
        total_price=product.price, 
        status='pending'
    )
    
    #  Tạo chi tiết đơn hàng
    OrderItem.objects.create(
        order=order,          
        product=product,      
        price=product.price,  
        quantity=1            
    )
    
    # 4. Thông báo và chuyển hướng
    messages.success(request, f"Đã đặt mua thành công: {product.name}!")
    return redirect('home')
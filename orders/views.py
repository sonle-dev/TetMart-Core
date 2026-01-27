from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product 
# 👇 Quan trọng: Phải import thêm OrderItem
from .models import Order, OrderItem 

# xu li mua ngay
@login_required(login_url='login')
def buy_now_view(request, product_id):
    # Lấy sản phẩm
    product = get_object_or_404(Product, id=product_id)
    
    # Lấy số lượng từ Form gửi lên 

    try:
        qty_from_html = request.POST.get('quantity', 1)
        quantity = int(qty_from_html)
        if quantity < 1: quantity = 1 # Không cho âm 
    except:
        quantity = 1

    # gia x so luong
    total_bill = product.price * quantity

    # tạo Order
    order = Order.objects.create(
        user=request.user,
        total_price=total_bill, 
        status='pending'
    )
    
    # Tạo OrderItem
    OrderItem.objects.create(
        order=order,          
        product=product,      
        price=product.price,  
        quantity=quantity     
    )
    
    messages.success(request, f"Đã đặt mua {quantity} sản phẩm: {product.name}!")
    return redirect('home')
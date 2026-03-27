from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from products.models import Product
from orders.models import Order, OrderItem


@login_required(login_url='login')
def buy_now_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    try:
        qty_from_html = request.POST.get('quantity', 1)
        quantity = int(qty_from_html)
        if quantity < 1:
            quantity = 1
    except:
        quantity = 1

    total_bill = product.price * quantity

    user = request.user
    full_name = getattr(user, 'username', 'Khách hàng')
    phone = getattr(user, 'phone', '') or 'Chưa cập nhật'
    address = getattr(user, 'address', '') or 'Chưa cập nhật'

    order = Order.objects.create(
        user=user,
        full_name=full_name,
        phone=phone,
        address=address,
        note='Đơn mua ngay',
        total_price=total_bill,
        status='pending'
    )

    OrderItem.objects.create(
        order=order,
        product=product,
        price=product.price,
        quantity=quantity
    )

    messages.success(request, f"Đã đặt mua {quantity} sản phẩm: {product.name}!")
    return redirect('dashboard_orders')
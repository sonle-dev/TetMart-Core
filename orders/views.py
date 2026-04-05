from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Order, OrderItem


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

    request.session['checkout_mode'] = 'buy_now'
    request.session['buy_now_product_id'] = product.id
    request.session['buy_now_quantity'] = quantity

    return redirect('orders:checkout')


@login_required(login_url='login')
def checkout_view(request):
    checkout_mode = request.session.get('checkout_mode')
    items = []
    total_quantity = 0
    total_price = 0

    form_data = {
        'full_name': getattr(request.user, 'username', '') or '',
        'phone': getattr(request.user, 'phone', '') or '',
        'address': getattr(request.user, 'address', '') or '',
        'note': '',
        'payment_method': 'cod',
    }

    if checkout_mode == 'buy_now':
        product_id = request.session.get('buy_now_product_id')
        quantity = request.session.get('buy_now_quantity', 1)

        if not product_id:
            messages.error(request, 'Không có sản phẩm để thanh toán.')
            return redirect('home')

        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity

        items.append({
            'product': product,
            'image': getattr(product, 'image', ''),
            'name': product.name,
            'category': getattr(product.category, 'name', str(product.category)),
            'quantity': quantity,
            'subtotal': subtotal,
            'subtotal_display': f"{int(subtotal):,}".replace(",", "."),
        })

        total_quantity = quantity
        total_price = subtotal

    else:
        cart = request.session.get('cart', {})

        if not cart:
            messages.error(request, 'Giỏ hàng đang trống.')
            return redirect('cart:detail')

        products = Product.objects.filter(id__in=cart.keys())

        for product in products:
            cart_item = cart.get(str(product.id), {})
            quantity = int(cart_item.get('quantity', 0))

            if quantity < 1:
                continue

            subtotal = product.price * quantity

            items.append({
                'product': product,
                'image': getattr(product, 'image', ''),
                'name': product.name,
                'category': getattr(product.category, 'name', str(product.category)),
                'quantity': quantity,
                'subtotal': subtotal,
                'subtotal_display': f"{int(subtotal):,}".replace(",", "."),
            })

            total_quantity += quantity
            total_price += subtotal

    context = {
        'form_data': form_data,
        'items': items,
        'total_quantity': total_quantity,
        'total_price': total_price,
        'total_price_display': f"{int(total_price):,}".replace(",", "."),
    }
    return render(request, 'orders/checkout.html', context)


@login_required(login_url='login')
def place_order_view(request):
    if request.method != 'POST':
        return redirect('orders:checkout')

    checkout_mode = request.session.get('checkout_mode')
    user = request.user

    full_name = request.POST.get('full_name', '').strip() or getattr(user, 'username', 'Khách hàng')
    phone = request.POST.get('phone', '').strip() or getattr(user, 'phone', '') or 'Chưa cập nhật'
    address = request.POST.get('address', '').strip() or getattr(user, 'address', '') or 'Chưa cập nhật'
    note = request.POST.get('note', '').strip() or 'Đơn đặt hàng'

    order = Order.objects.create(
        user=user,
        full_name=full_name,
        phone=phone,
        address=address,
        note=note,
        total_price=0,
        status='new'
    )

    total_bill = 0

    if checkout_mode == 'buy_now':
        product_id = request.session.get('buy_now_product_id')
        quantity = int(request.session.get('buy_now_quantity', 1))

        if not product_id:
            messages.error(request, 'Không có sản phẩm để đặt hàng.')
            order.delete()
            return redirect('orders:checkout')

        product = get_object_or_404(Product, id=product_id)

        OrderItem.objects.create(
            order=order,
            product=product,
            price=product.price,
            quantity=quantity
        )

        total_bill += product.price * quantity

        request.session.pop('buy_now_product_id', None)
        request.session.pop('buy_now_quantity', None)

    else:
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, 'Giỏ hàng đang trống.')
            order.delete()
            return redirect('cart:detail')

        products = Product.objects.filter(id__in=cart.keys())

        for product in products:
            cart_item = cart.get(str(product.id), {})
            quantity = int(cart_item.get('quantity', 0))

            if quantity < 1:
                continue

            OrderItem.objects.create(
                order=order,
                product=product,
                price=product.price,
                quantity=quantity
            )

            total_bill += product.price * quantity

        request.session['cart'] = {}

    order.total_price = total_bill
    order.save()

    request.session.pop('checkout_mode', None)

    messages.success(request, 'Đặt hàng thành công.')
    return redirect('dashboard_orders')
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from products.models import Product
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from orders.models import Order, OrderItem



def cart_detail(request):
    cart = request.session.get("cart", {})
    items = []
    total_price = 0
    total_quantity = 0

    for product_id, item in cart.items():
        if isinstance(item, int):
            product = get_object_or_404(Product, id=product_id)
            quantity = item
            price = float(product.price)
            image = product.image.url if product.image else ""
            name = product.name
            slug = product.slug
            category = product.category.name if product.category else ""
        else:
            quantity = item.get("quantity", 0)
            price = float(item.get("price", 0))
            image = item.get("image", "")
            name = item.get("name", "")
            slug = item.get("slug", "")
            category = item.get("category", "")

            if not category:
                product = get_object_or_404(Product, id=product_id)
                category = product.category.name if product.category else ""

        subtotal = price * quantity
        total_price += subtotal
        total_quantity += quantity

        items.append({
            "id": product_id,
            "name": name,
            "price": price,
            "price_display": f"{int(price):,}".replace(",", "."),
            "quantity": quantity,
            "image": image,
            "slug": slug,
            "category": category,
            "subtotal": subtotal,
            "subtotal_display": f"{int(subtotal):,}".replace(",", "."),
        })

    context = {
        "items": items,
        "total_quantity": total_quantity,
        "total_price": total_price,
        "total_price_display": f"{int(total_price):,}".replace(",", "."),
    }

    return render(request, "cart/cart_detail.html", context)


def add(request, product_id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Phương thức không hợp lệ"}, status=405)

    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get("cart", {})
    product_id_str = str(product.id)
    quantity = int(request.POST.get("quantity", 1))

    if product_id_str in cart and isinstance(cart[product_id_str], int):
        old_quantity = cart[product_id_str]
        cart[product_id_str] = {
            "name": product.name,
            "price": float(product.price),
            "quantity": old_quantity + quantity,
            "image": product.image.url if product.image else "",
            "slug": product.slug,
            "category": product.category.name if product.category else "",
        }
    elif product_id_str in cart and isinstance(cart[product_id_str], dict):
        cart[product_id_str]["quantity"] += quantity
    else:
        cart[product_id_str] = {
            "name": product.name,
            "price": float(product.price),
            "quantity": quantity,
            "image": product.image.url if product.image else "",
            "slug": product.slug,
            "category": product.category.name if product.category else "",
        }

    request.session["cart"] = cart
    request.session.modified = True

    cart_total_quantity = 0
    for item in cart.values():
        if isinstance(item, dict):
            cart_total_quantity += item.get("quantity", 0)
        elif isinstance(item, int):
            cart_total_quantity += item

    return JsonResponse({
        "success": True,
        "message": "Đã thêm vào giỏ hàng",
        "cart_total_quantity": cart_total_quantity,
    })


def update(request, item_id):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        quantity = int(request.POST.get("quantity", 1))

        if item_id in cart:
            if isinstance(cart[item_id], int):
                cart[item_id] = quantity
            else:
                cart[item_id]["quantity"] = quantity

        request.session["cart"] = cart
        request.session.modified = True

    return redirect("cart:detail")


def remove(request, item_id):
    cart = request.session.get("cart", {})

    if item_id in cart:
        del cart[item_id]

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart:detail")


def clear(request):
    request.session["cart"] = {}
    request.session.modified = True
    return redirect("cart:detail")

@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)

    if request.method != "POST":
        return redirect("products:product_detail", product_id=product.id)

    quantity = int(request.POST.get("quantity", 1))

    if quantity < 1:
        quantity = 1

    if product.stock < quantity:
        messages.error(request, "Số lượng vượt quá tồn kho.")
        return redirect("products:product_detail", product_id=product.id)

    total = product.price * quantity

    order = Order.objects.create(
        user=request.user,
        full_name=request.user.get_full_name() or request.user.username,
        phone=getattr(request.user, "phone", "") or "Chưa cập nhật",
        address=getattr(request.user, "address", "") or "Chưa cập nhật",
        total_price=total,
        status="new",
    )

    OrderItem.objects.create(
        order=order,
        product=product,
        price=product.price,
        quantity=quantity,
    )

    product.stock -= quantity
    product.save()

    messages.success(request, "Mua ngay thành công!")
    return redirect("cart:detail")
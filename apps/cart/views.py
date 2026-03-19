from django.shortcuts import render, redirect
from products.models import Product


def cart_detail(request):
    cart = request.session.get("cart", {})
    items = []
    total_quantity = 0
    total_price = 0

    if cart:
        product_ids = cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            quantity = cart.get(str(product.id), 0)
            subtotal = product.price * quantity

            items.append({
                "id": product.id,
                "name": product.name,
                "image": product.image.url if product.image else "",
                "category": product.category.name if product.category else "Chưa phân loại",
                "price_display": f"{int(product.price):,}".replace(",", "."),
                "quantity": quantity,
                "subtotal_display": f"{int(subtotal):,}".replace(",", "."),
                "slug": product.slug,
            })

            total_quantity += quantity
            total_price += subtotal

    context = {
        "items": items,
        "total_quantity": total_quantity,
        "total_price_display": f"{int(total_price):,}".replace(",", "."),
    }
    return render(request, "cart/cart_detail.html", context)


def add(request, product_id):
    cart = request.session.get("cart", {})
    product_id = str(product_id)

    quantity = int(request.POST.get("quantity", 1))

    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity

    request.session["cart"] = cart
    return redirect("cart:detail")


def update(request, product_id):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        product_id = str(product_id)
        quantity = int(request.POST.get("quantity", 1))

        if quantity > 0:
            cart[product_id] = quantity
        else:
            cart.pop(product_id, None)

        request.session["cart"] = cart

    return redirect("cart:detail")


def remove(request, product_id):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        product_id = str(product_id)
        cart.pop(product_id, None)
        request.session["cart"] = cart

    return redirect("cart:detail")


def clear(request):
    if request.method == "POST":
        request.session["cart"] = {}

    return redirect("cart:detail")
# apps/cart/views.py

from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.http import JsonResponse
from .utils import (
    build_cart_context,
    get_cart,
    get_product_by_id,
    save_cart,
    get_cart_total_quantity,
)

def cart_detail(request):
    context = build_cart_context(request)
    return render(request, "cart/cart_detail.html", context)


def add_to_cart(request, product_id):
    is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"

    if request.method != "POST":
        if is_ajax:
            return JsonResponse(
                {"success": False, "message": "Phương thức không hợp lệ."},
                status=405
            )
        return redirect("core:product_detail", product_id=product_id)

    product = get_product_by_id(product_id)
    if not product:
        if is_ajax:
            return JsonResponse(
                {"success": False, "message": "Sản phẩm không tồn tại."},
                status=404
            )
        messages.error(request, "Sản phẩm không tồn tại.")
        return redirect("core:home")

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1

    quantity = max(1, quantity)

    cart = get_cart(request)
    key = str(product_id)

    try:
        current_quantity = int(cart.get(key, 0))
    except (TypeError, ValueError):
        current_quantity = 0

    cart[key] = current_quantity + quantity
    save_cart(request, cart)

    success_message = f"Đã thêm {quantity} x {product['name']} vào giỏ hàng."
    cart_total_quantity = get_cart_total_quantity(request)

    if is_ajax:
        return JsonResponse({
            "success": True,
            "message": success_message,
            "cart_total_quantity": cart_total_quantity,
        })

    messages.success(request, success_message)

    next_url = request.POST.get("next", "")
    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(next_url)

    return redirect("cart:detail")


def update_cart_item(request, product_id):
    if request.method != "POST":
        return redirect("cart:detail")

    cart = get_cart(request)
    key = str(product_id)

    if key not in cart:
        messages.error(request, "Sản phẩm không có trong giỏ hàng.")
        return redirect("cart:detail")

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1

    if quantity <= 0:
        cart.pop(key, None)
        messages.success(request, "Đã xóa sản phẩm khỏi giỏ hàng.")
    else:
        cart[key] = quantity
        messages.success(request, "Đã cập nhật số lượng sản phẩm.")

    save_cart(request, cart)
    return redirect("cart:detail")


def remove_from_cart(request, product_id):
    if request.method != "POST":
        return redirect("cart:detail")

    cart = get_cart(request)
    key = str(product_id)

    if key in cart:
        cart.pop(key)
        save_cart(request, cart)
        messages.success(request, "Đã xóa sản phẩm khỏi giỏ hàng.")
    else:
        messages.error(request, "Sản phẩm không có trong giỏ hàng.")

    return redirect("cart:detail")


def clear_cart(request):
    if request.method != "POST":
        return redirect("cart:detail")

    save_cart(request, {})
    messages.success(request, "Đã xóa toàn bộ giỏ hàng.")
    return redirect("cart:detail")
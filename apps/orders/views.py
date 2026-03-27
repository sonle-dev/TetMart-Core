from django.contrib import messages
from django.shortcuts import redirect, render

from apps.cart.utils import build_cart_context, save_cart


def checkout_view(request):
    context = build_cart_context(request)

    if not context.get("items"):
        messages.error(request, "Giỏ hàng đang trống. Vui lòng thêm sản phẩm trước khi thanh toán.")
        return redirect("cart:detail")

    if request.method == "POST":
        full_name = (request.POST.get("full_name") or "").strip()
        phone = (request.POST.get("phone") or "").strip()
        address = (request.POST.get("address") or "").strip()
        note = (request.POST.get("note") or "").strip()
        payment_method = (request.POST.get("payment_method") or "cod").strip()

        errors = []
        if not full_name:
            errors.append("Vui lòng nhập họ và tên.")
        if not phone:
            errors.append("Vui lòng nhập số điện thoại.")
        if not address:
            errors.append("Vui lòng nhập địa chỉ nhận hàng.")

        if errors:
            for err in errors:
                messages.error(request, err)
            context["form_data"] = {
                "full_name": full_name,
                "phone": phone,
                "address": address,
                "note": note,
                "payment_method": payment_method,
            }
            return render(request, "orders/checkout.html", context)

        # Mock xử lý đặt hàng ở nhánh frontend
        order_preview = {
            "customer_name": full_name,
            "phone": phone,
            "address": address,
            "note": note,
            "payment_method": payment_method,
            "total_quantity": context["total_quantity"],
            "total_price_display": context["total_price_display"],
            "items": context["items"],
        }

        request.session["last_order_preview"] = order_preview
        save_cart(request, {})
        return redirect("orders:success")

    context["form_data"] = {
        "full_name": "",
        "phone": "",
        "address": "",
        "note": "",
        "payment_method": "cod",
    }
    return render(request, "orders/checkout.html", context)


def order_success_view(request):
    order_preview = request.session.get("last_order_preview")
    if not order_preview:
        messages.error(request, "Không tìm thấy thông tin đơn hàng gần nhất.")
        return redirect("core:home")

    return render(
        request,
        "orders/order_success.html",
        {"order": order_preview},
    )
from django.contrib import messages
from django.shortcuts import redirect, render

from apps.cart.utils import build_cart_context, save_cart


BANK_TRANSFER_INFO = {
    "bank_name": "Ngân hàng TMCP Ngoại thương Việt Nam (Vietcombank)",
    "account_number": "1234567890",
    "account_name": "TET MART COMPANY",
    "branch": "Chi nhánh Thái Nguyên",
}


def _build_order_preview(context, full_name, phone, address, note, payment_method):
    return {
        "customer_name": full_name,
        "phone": phone,
        "address": address,
        "note": note,
        "payment_method": payment_method,
        "total_quantity": context["total_quantity"],
        "total_price": context["total_price"],
        "total_price_display": context["total_price_display"],
        "items": context["items"],
    }


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
            for error in errors:
                messages.error(request, error)

            context["form_data"] = {
                "full_name": full_name,
                "phone": phone,
                "address": address,
                "note": note,
                "payment_method": payment_method,
            }
            return render(request, "orders/checkout.html", context)

        order_preview = _build_order_preview(
            context=context,
            full_name=full_name,
            phone=phone,
            address=address,
            note=note,
            payment_method=payment_method,
        )

        if payment_method == "bank":
            transfer_content = f"TETMART {phone[-4:] if len(phone) >= 4 else phone}"
            request.session["pending_bank_order"] = {
                **order_preview,
                "transfer_content": transfer_content,
            }
            request.session.modified = True
            return redirect("orders:bank_transfer")

        request.session["last_order_preview"] = order_preview
        request.session.modified = True
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


def bank_transfer_view(request):
    pending_order = request.session.get("pending_bank_order")

    if not pending_order:
        messages.error(request, "Không tìm thấy đơn hàng chờ chuyển khoản.")
        return redirect("orders:checkout")

    context = {
        "order": pending_order,
        "bank_info": BANK_TRANSFER_INFO,
    }
    return render(request, "orders/bank_transfer_info.html", context)


def confirm_bank_transfer_view(request):
    if request.method != "POST":
        return redirect("orders:checkout")

    pending_order = request.session.get("pending_bank_order")

    if not pending_order:
        messages.error(request, "Không tìm thấy đơn hàng chờ chuyển khoản.")
        return redirect("orders:checkout")

    request.session["last_order_preview"] = pending_order
    request.session.pop("pending_bank_order", None)
    request.session.modified = True

    save_cart(request, {})
    messages.success(request, "Đã ghi nhận thông tin chuyển khoản của bạn.")
    return redirect("orders:success")


def order_success_view(request):
    order_preview = request.session.get("last_order_preview")

    if not order_preview:
        messages.error(request, "Không tìm thấy thông tin đơn hàng gần nhất.")
        return redirect("core:home")

    return render(request, "orders/order_success.html", {"order": order_preview})
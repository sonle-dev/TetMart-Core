from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from apps.cart.utils import get_cart, save_cart
from .mock_data import product_reviews_data, products_data


def get_daily_suggestions():
    if not products_data:
        return []
    return [dict(product) for product in products_data[:4]]


def build_product_reviews(product_id):
    raw_reviews = product_reviews_data.get(product_id, [])
    reviews = []
    total_rating = 0

    for item in raw_reviews:
        rating = max(1, min(5, int(item.get("rating", 5))))
        total_rating += rating
        reviews.append(
            {
                **item,
                "rating": rating,
                "filled_stars": range(rating),
                "empty_stars": range(5 - rating),
            }
        )

    review_total = len(reviews)
    average_rating = round(total_rating / review_total, 1) if review_total else 0
    average_star_count = max(0, min(5, round(average_rating)))

    rating_breakdown = []
    for star in range(5, 0, -1):
        count = sum(1 for review in reviews if review["rating"] == star)
        percent = int((count / review_total) * 100) if review_total else 0
        rating_breakdown.append(
            {
                "star": star,
                "count": count,
                "percent": percent,
            }
        )

    return {
        "reviews": reviews,
        "review_total": review_total,
        "average_rating": f"{average_rating:.1f}" if review_total else "0.0",
        "average_full_stars": range(average_star_count),
        "average_empty_stars": range(5 - average_star_count),
        "rating_breakdown": rating_breakdown,
    }


def _to_int_price(value):
    try:
        cleaned = str(value).replace(".", "").replace(",", "").replace("đ", "").strip()
        return int(cleaned)
    except Exception:
        return None


def _get_product_or_404(product_id):
    product = next((item for item in products_data if item["id"] == product_id), None)
    if not product:
        raise Http404("Sản phẩm không tồn tại")
    return product


def _build_account_profile(user):
    full_name = user.get_full_name().strip() if user.get_full_name() else user.username
    initial = (user.username[:1] if user.username else "U").upper()

    return {
        "full_name": full_name,
        "username": user.username,
        "email": user.email,
        "phone": "0987 654 321",
        "address": "ĐH CNTT & TT Thái Nguyên",
        "avatar_url": "",
        "avatar_initial": initial,
        "joined_at": user.date_joined,
        "is_staff": user.is_staff,
    }


def _build_my_orders():
    return [
        {
            "id": "DH001",
            "status": "pending",
            "status_label": "Chờ xác nhận",
            "status_class": "warning",
            "created_at": "20/04/2026",
            "total_display": "330.000",
            "items_count": 2,
            "payment_method": "Thanh toán khi nhận hàng",
            "shipping_address": "ĐH CNTT & TT Thái Nguyên",
            "can_reorder": False,
            "can_cancel": True,
            "items": [
                {
                    "product_id": 1,
                    "name": "Đèn lồng đỏ truyền thống",
                    "quantity": 1,
                    "price_display": "150.000",
                    "icon": "🏮",
                },
                {
                    "product_id": 2,
                    "name": "Cành hoa mai vàng",
                    "quantity": 1,
                    "price_display": "180.000",
                    "icon": "🌸",
                },
            ],
        },
        {
            "id": "DH002",
            "status": "processing",
            "status_label": "Đang xử lý",
            "status_class": "info",
            "created_at": "19/04/2026",
            "total_display": "250.000",
            "items_count": 1,
            "payment_method": "Chuyển khoản",
            "shipping_address": "88 Lê Lợi, Q.1, TP.HCM",
            "can_reorder": False,
            "can_cancel": True,
            "items": [
                {
                    "product_id": 3,
                    "name": "Bao lì xì hoa mai vàng",
                    "quantity": 10,
                    "price_display": "25.000",
                    "icon": "🧧",
                },
            ],
        },
        {
            "id": "DH003",
            "status": "shipping",
            "status_label": "Đang giao",
            "status_class": "primary",
            "created_at": "18/04/2026",
            "total_display": "195.000",
            "items_count": 2,
            "payment_method": "Thanh toán khi nhận hàng",
            "shipping_address": "25 Hai Bà Trưng, Đà Nẵng",
            "can_reorder": False,
            "can_cancel": False,
            "items": [
                {
                    "product_id": 4,
                    "name": "Dây treo trang trí Tết",
                    "quantity": 1,
                    "price_display": "45.000",
                    "icon": "🎊",
                },
                {
                    "product_id": 1,
                    "name": "Đèn lồng đỏ truyền thống",
                    "quantity": 1,
                    "price_display": "150.000",
                    "icon": "🏮",
                },
            ],
        },
        {
            "id": "DH004",
            "status": "completed",
            "status_label": "Hoàn thành",
            "status_class": "success",
            "created_at": "15/04/2026",
            "total_display": "180.000",
            "items_count": 1,
            "payment_method": "Chuyển khoản",
            "shipping_address": "15 Trần Phú, Huế",
            "can_reorder": True,
            "can_cancel": False,
            "items": [
                {
                    "product_id": 2,
                    "name": "Cành hoa mai vàng",
                    "quantity": 1,
                    "price_display": "180.000",
                    "icon": "🌸",
                },
            ],
        },
        {
            "id": "DH005",
            "status": "cancelled",
            "status_label": "Đã hủy",
            "status_class": "danger",
            "created_at": "12/04/2026",
            "total_display": "45.000",
            "items_count": 1,
            "payment_method": "Thanh toán khi nhận hàng",
            "shipping_address": "7 Pasteur, TP.HCM",
            "can_reorder": True,
            "can_cancel": False,
            "items": [
                {
                    "product_id": 4,
                    "name": "Dây treo trang trí Tết",
                    "quantity": 1,
                    "price_display": "45.000",
                    "icon": "🎊",
                },
            ],
        },
    ]


def _get_my_order_or_none(order_id, orders):
    return next((order for order in orders if order["id"] == order_id), None)


@login_required(login_url="core:login")
def my_orders_view(request):
    orders = _build_my_orders()
    cancelled_order_ids = request.session.get("cancelled_order_ids", [])

    for order in orders:
        if order["id"] in cancelled_order_ids:
            order["status"] = "cancelled"
            order["status_label"] = "Đã hủy"
            order["status_class"] = "danger"
            order["can_cancel"] = False
            order["can_reorder"] = True

    context = {
        "my_orders": orders,
    }
    return render(request, "user/orders.html", context)


@login_required(login_url="core:login")
def reorder_order_view(request, order_id):
    if request.method != "POST":
        return redirect("core:my_orders")

    orders = _build_my_orders()
    cancelled_order_ids = request.session.get("cancelled_order_ids", [])

    for order in orders:
        if order["id"] in cancelled_order_ids:
            order["status"] = "cancelled"
            order["status_label"] = "Đã hủy"
            order["status_class"] = "danger"
            order["can_cancel"] = False
            order["can_reorder"] = True

    order = _get_my_order_or_none(order_id, orders)
    if not order:
        messages.error(request, "Không tìm thấy đơn hàng để mua lại.")
        return redirect("core:my_orders")

    if not order.get("can_reorder"):
        messages.error(request, "Đơn hàng này chưa thể mua lại.")
        return redirect("core:my_orders")

    cart = get_cart(request)

    for item in order.get("items", []):
        product_id = item.get("product_id")
        quantity = int(item.get("quantity", 1))
        key = str(product_id)

        try:
            current_quantity = int(cart.get(key, 0))
        except (TypeError, ValueError):
            current_quantity = 0

        cart[key] = current_quantity + quantity

    save_cart(request, cart)
    messages.success(request, f"Đã thêm lại sản phẩm từ đơn {order_id} vào giỏ hàng.")
    return redirect("cart:detail")


@login_required(login_url="core:login")
def cancel_order_view(request, order_id):
    if request.method != "POST":
        return redirect("core:my_orders")

    orders = _build_my_orders()
    cancelled_order_ids = request.session.get("cancelled_order_ids", [])
    order = _get_my_order_or_none(order_id, orders)

    if not order:
        messages.error(request, "Không tìm thấy đơn hàng.")
        return redirect("core:my_orders")

    if order["id"] in cancelled_order_ids:
        messages.info(request, f"Đơn {order_id} đã được hủy trước đó.")
        return redirect("core:my_orders")

    if not order.get("can_cancel"):
        messages.error(request, "Đơn hàng này không thể hủy.")
        return redirect("core:my_orders")

    cancelled_order_ids.append(order_id)
    request.session["cancelled_order_ids"] = cancelled_order_ids
    request.session.modified = True

    messages.success(request, f"Đã hủy đơn hàng {order_id}.")
    return redirect("core:my_orders")


def index(request):
    context = {
        "products": products_data,
        "daily_suggestions": get_daily_suggestions(),
    }
    return render(request, "index.html", context)


def product_list_view(request):
    q = (request.GET.get("q") or "").strip().lower()
    category = (request.GET.get("category") or "all").strip()
    price_min = request.GET.get("price_min") or ""
    price_max = request.GET.get("price_max") or ""
    sort = request.GET.get("sort") or "newest"

    products = list(products_data)
    categories = sorted({p.get("category") for p in products if p.get("category")})

    if q:
        products = [p for p in products if q in p.get("name", "").lower()]

    if category and category != "all":
        products = [p for p in products if p.get("category") == category]

    min_value = _to_int_price(price_min) if price_min else None
    max_value = _to_int_price(price_max) if price_max else None

    if min_value is not None:
        products = [p for p in products if (_to_int_price(p.get("price")) or 0) >= min_value]

    if max_value is not None:
        products = [p for p in products if (_to_int_price(p.get("price")) or 0) <= max_value]

    if sort == "price_asc":
        products.sort(key=lambda p: _to_int_price(p.get("price")) or 10**18)
    elif sort == "price_desc":
        products.sort(key=lambda p: _to_int_price(p.get("price")) or -1, reverse=True)

    context = {
        "products": products,
        "categories": categories,
        "filters": {
            "q": request.GET.get("q", ""),
            "category": category,
            "price_min": request.GET.get("price_min", ""),
            "price_max": request.GET.get("price_max", ""),
            "sort": sort,
        },
    }
    return render(request, "product_list.html", context)


def product_detail(request, product_id):
    product = _get_product_or_404(product_id)
    review_context = build_product_reviews(product_id)

    context = {
        "product": product,
        **review_context,
    }
    return render(request, "product_detail.html", context)


def register_view(request):
    if request.method == "POST":
        messages.success(request, "Đăng ký tài khoản thành công! Vui lòng đăng nhập.")
        return redirect("core:login")

    return render(request, "user/register.html")


def login_view(request):
    if request.method == "POST":
        username_input = request.POST.get("username")
        password_input = request.POST.get("password")

        user = authenticate(request, username=username_input, password=password_input)

        if user is not None:
            login(request, user)
            messages.success(request, f"Chào mừng {user.username} quay trở lại!")

            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)

            return redirect("core:home")

        messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng!")

    return render(request, "user/login.html")


@login_required(login_url="core:login")
def account_view(request):
    account_profile = _build_account_profile(request.user)

    if request.method == "POST":
        account_profile = {
            **account_profile,
            "full_name": f"{request.POST.get('first_name', '').strip()} {request.POST.get('last_name', '').strip()}".strip()
            or request.user.username,
            "username": request.POST.get("username", request.user.username).strip() or request.user.username,
            "email": request.POST.get("email", request.user.email).strip(),
            "phone": request.POST.get("phone", "").strip(),
            "address": request.POST.get("address", "").strip(),
        }
        messages.success(request, "Đã lưu giao diện thông tin tài khoản.")

    full_name_parts = account_profile["full_name"].split()
    first_name = full_name_parts[0] if full_name_parts else ""
    last_name = " ".join(full_name_parts[1:]) if len(full_name_parts) > 1 else ""

    context = {
        "account_profile": account_profile,
        "form_data": {
            "first_name": first_name,
            "last_name": last_name,
            "username": account_profile["username"],
            "email": account_profile["email"],
            "phone": account_profile["phone"],
            "address": account_profile["address"],
        },
    }
    return render(request, "user/account.html", context)


@login_required(login_url="core:login")
def my_orders_view(request):
    context = {
        "my_orders": _build_my_orders(),
    }
    return render(request, "user/orders.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, "Đăng xuất thành công! Hẹn gặp lại. 👋")
    return redirect("core:login")
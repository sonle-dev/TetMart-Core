from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.shortcuts import redirect, render

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


def logout_view(request):
    logout(request)
    messages.success(request, "Đăng xuất thành công! Hẹn gặp lại. 👋")
    return redirect("core:login")
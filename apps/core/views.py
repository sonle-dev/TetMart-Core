from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import Http404


# 1. TẠO KHO DỮ LIỆU GIẢ (MOCK DATA)
from django.shortcuts import render
from django.http import Http404


products_data = [
    {
        "id": 1,
        "name": "Đèn lồng đỏ truyền thống",
        "price": "150.000",
        "category": "Đèn lồng",
        "image": "https://...",
        "icon": "🏮",
    },
    {
        "id": 2,
        "name": "Cành hoa mai vàng",
        "price": "180.000",
        "category": "Hoa mai/đào",
        "image": "https://...",
        "icon": "🌸",
    },
    {
        "id": 3,
        "name": "Bao lì xì hoa mai vàng",
        "price": "25.000",
        "category": "Bao lì xì",
        "image": "https://...",
        "icon": "🧧",
    },
    {
        "id": 4,
        "name": "Dây treo trang trí Tết",
        "price": "45.000",
        "category": "Dây trang trí",
        "image": "https://...",
        "icon": "🎊",
    },
]   # <- PHẢI CÓ DÒNG NÀY ĐỂ ĐÓNG products_data


product_reviews_data = {
    1: [
        {
            "name": "Nguyễn Hoàng Phúc",
            "rating": 5,
            "comment": "Đèn lồng đẹp, màu đỏ tươi, chất liệu ổn. Treo lên nhìn rất nổi bật và đúng như mô tả.",
            "created_at": "12/03/2026",
            "verified_purchase": True,
        },
        {
            "name": "Trần Mỹ Linh",
            "rating": 4,
            "comment": "Đóng gói kỹ, sản phẩm đẹp. Mình mong dây treo dày hơn một chút thì sẽ tốt hơn.",
            "created_at": "09/03/2026",
            "verified_purchase": True,
        },
    ],
    2: [
        {
            "name": "Phạm Thu Hà",
            "rating": 5,
            "comment": "Cành hoa mai lên màu đẹp, chụp ảnh rất ấn tượng. Để trang trí phòng khách rất hợp.",
            "created_at": "13/03/2026",
            "verified_purchase": True,
        },
    ],
    3: [
        {
            "name": "Võ Thành Đạt",
            "rating": 5,
            "comment": "Bao lì xì giấy cứng, màu in đẹp, cầm tay chắc chắn. Rất đáng tiền.",
            "created_at": "11/03/2026",
            "verified_purchase": True,
        },
    ],
    4: [
        {
            "name": "Huỳnh Gia Hân",
            "rating": 4,
            "comment": "Dây treo đẹp, lên hình ổn. Màu sắc giống ảnh và dễ lắp đặt.",
            "created_at": "10/03/2026",
            "verified_purchase": True,
        },
    ],
}
def get_daily_suggestions():
    if not products_data:
        return []

    return [dict(product) for product in products_data[:4]]

    day_seed = date.today().timetuple().tm_yday
    shift = day_seed % len(suggestions)
    rotated = suggestions[shift:] + suggestions[:shift]

    daily_notes = [
        "Gợi ý nổi bật hôm nay",
        "Dễ phối cùng không gian Tết",
        "Món đáng mua trong ngày",
        "Phù hợp trang trí nhanh",
    ]

    selected = rotated[:4]

    for idx, product in enumerate(selected):
        product["daily_note"] = daily_notes[idx % len(daily_notes)]

    return selected

def build_product_reviews(product_id):
    raw_reviews = product_reviews_data.get(product_id, [])
    reviews = []
    total_rating = 0

    for item in raw_reviews:
        rating = max(1, min(5, int(item.get("rating", 5))))
        total_rating += rating

        reviews.append({
            **item,
            "rating": rating,
            "filled_stars": range(rating),
            "empty_stars": range(5 - rating),
        })

    review_total = len(reviews)
    average_rating = round(total_rating / review_total, 1) if review_total else 0
    average_star_count = max(0, min(5, round(average_rating)))

    rating_breakdown = []
    for star in range(5, 0, -1):
        count = sum(1 for review in reviews if review["rating"] == star)
        percent = int((count / review_total) * 100) if review_total else 0
        rating_breakdown.append({
            "star": star,
            "count": count,
            "percent": percent,
        })

    return {
        "reviews": reviews,
        "review_total": review_total,
        "average_rating": f"{average_rating:.1f}" if review_total else "0.0",
        "average_full_stars": range(average_star_count),
        "average_empty_stars": range(5 - average_star_count),
        "rating_breakdown": rating_breakdown,
    }


def product_detail(request, product_id):
    product = next((item for item in products_data if item["id"] == product_id), None)
    if not product:
        raise Http404("Sản phẩm không tồn tại")

    review_context = build_product_reviews(product_id)

    context = {
        "product": product,
        **review_context,
    }
    return render(request, "product_detail.html", context)

# ===== Helper: parse price =====
def _to_int_price(x):
    """
    Convert '150.000' / '150,000' / '150000' -> 150000 (int)
    """
    try:
        s = str(x).replace(".", "").replace(",", "").replace("đ", "").strip()
        return int(s)
    except Exception:
        return None


# Hàm hiển thị trang chủ
def index(request):
    context = {
    "products": products_data,
    "daily_suggestions": get_daily_suggestions(),
}

    return render(request, "index.html", context)


# ✅ Trang danh sách sản phẩm (có bộ lọc + search + sort)
def product_list_view(request):
    # GET params
    q = (request.GET.get("q") or "").strip().lower()
    category = (request.GET.get("category") or "all").strip()
    price_min = request.GET.get("price_min") or ""
    price_max = request.GET.get("price_max") or ""
    sort = request.GET.get("sort") or "newest"

    products = list(products_data)

    # Danh sách danh mục cho dropdown
    categories = sorted({p.get("category") for p in products if p.get("category")})

    # 1) Search theo tên sản phẩm
    if q:
        products = [p for p in products if q in (p.get("name", "").lower())]

    # 2) Filter theo danh mục
    if category and category != "all":
        products = [p for p in products if p.get("category") == category]

    # 3) Filter theo khoảng giá
    min_v = _to_int_price(price_min) if price_min else None
    max_v = _to_int_price(price_max) if price_max else None

    if min_v is not None:
        products = [p for p in products if (_to_int_price(p.get("price")) or 0) >= min_v]
    if max_v is not None:
        products = [p for p in products if (_to_int_price(p.get("price")) or 0) <= max_v]

    # 4) Sắp xếp
    # newest: mock chưa có created_at -> giữ nguyên
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


# Hàm hiển thị chi tiết sản phẩm
def product_detail(request, product_id):
    product = next((item for item in products_data if item["id"] == product_id), None)
    if not product:
        raise Http404("Sản phẩm không tồn tại")

    review_context = build_product_reviews(product_id)

    context = {
        "product": product,
        **review_context,
    }
    return render(request, "product_detail.html", context)

# ---------------------------------------------------------
# CÁC HÀM XỬ LÝ TÀI KHOẢN (Auth)
# ---------------------------------------------------------

def register_view(request):
    """Trang Đăng ký"""
    if request.method == "POST":
        # Logic lưu vào DB sẽ viết ở đây sau
        messages.success(request, "Đăng ký tài khoản thành công! Vui lòng đăng nhập.")
        return redirect("core:login")

    return render(request, "user/register.html")


def login_view(request):
    """Trang Đăng nhập"""
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
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng!")

    return render(request, "user/login.html")


def logout_view(request):
    """Xử lý Đăng xuất"""
    logout(request)
    messages.success(request, "Đăng xuất thành công! Hẹn gặp lại. 👋")
    return redirect("core:login")
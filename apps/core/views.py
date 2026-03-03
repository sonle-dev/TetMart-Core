from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import Http404

# 1. TẠO KHO DỮ LIỆU GIẢ (MOCK DATA)
products_data = [
    {
        'id': 1,
        'name': 'Đèn lồng đỏ truyền thống',
        'price': '150.000',
        'image': 'https://salt.tikicdn.com/cache/750x750/ts/product/d0/20/7a/12a86847c2310137452d921356247c18.jpg.webp',
        'category': 'Đèn lồng',
        'icon': '🏮',
        'desc': 'Đèn lồng vải nhung đỏ thắm, khung thép chắc chắn, mang lại may mắn.'
    },
    {
        'id': 2,
        'name': 'Cành hoa mai vàng',
        'price': '180.000',
        'image': 'https://bizweb.dktcdn.net/100/443/076/products/trang-tri-tet-hoa-dao-dong.jpg',
        'category': 'Hoa mai/đào',
        'icon': '🌸',
        'desc': 'Cành hoa mai giả cao cấp, màu sắc tươi tắn, bền đẹp suốt mùa Tết.'
    },
    {
        'id': 3,
        'name': 'Bao lì xì hoa mai vàng',
        'price': '25.000',
        'image': 'https://salt.tikicdn.com/cache/w1200/ts/product/6e/c8/10/7c462744d03d09a06655c65b5302636a.jpg',
        'category': 'Bao lì xì',
        'icon': '🧧',
        'desc': 'Combo 10 bao lì xì giấy cứng, in họa tiết rồng vàng sang trọng.'
    },
    {
        'id': 4,
        'name': 'Dây treo chữ Phúc',
        'price': '45.000',
        'image': 'https://vn-test-11.slatic.net/p/3c73499427b20387498c89599d14620f.jpg',
        'category': 'Dây trang trí',
        'icon': '🎊',
        'desc': 'Dây treo trang trí cửa nhà, mang ý nghĩa Phúc Lộc Thọ toàn gia.'
    }
]

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
    # Nếu trang chủ bạn chưa cần products thì có thể bỏ context.
    context = {
        "products": products_data,
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

    context = {"product": product}
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
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from products.models import Product, Category


# =========================
# HOME - LẤY DỮ LIỆU THẬT TỪ DATABASE
# =========================
def index(request):
    # Danh mục nổi bật (tuỳ bạn: all hoặc filter)
    categories = Category.objects.all()

    # Sản phẩm bán chạy / hiển thị trang chủ (tuỳ bạn: is_active=True hoặc all)
    products = Product.objects.filter(is_active=True)

    # Debug nhanh để biết có lấy được DB không
    print("DB categories:", categories.count())
    print("DB products:", products.count())

    context = {
        "categories": categories,
        "products": products,
    }
    return render(request, "index.html", context)


# =========================
# PRODUCT DETAIL - LẤY THẬT TỪ DATABASE
# =========================
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, "product_detail.html", {"product": product})


# =========================
# AUTH
# =========================
def register_view(request):
    if request.method == "POST":
        messages.success(request, "🎉 Đăng ký tài khoản thành công! Vui lòng đăng nhập.")
        return redirect("core:login")
    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        username_input = request.POST.get("username")
        password_input = request.POST.get("password")

        user = authenticate(request, username=username_input, password=password_input)
        if user is not None:
            login(request, user)
            messages.success(request, f"🎉 Chào mừng {user.username} quay trở lại!")
            return redirect("core:home")
        else:
            messages.error(request, "⚠️ Tên đăng nhập hoặc mật khẩu không đúng!")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "👋 Đăng xuất thành công! Hẹn gặp lại.")
    return redirect("core:login")


# =========================
# DASHBOARD
# =========================
@login_required(login_url="core:login")
def dashboard_view(request):
    context = {
        "total_orders": 150,
        "revenue": "25.000.000",
        "pending_orders": 5,
        "total_products": Product.objects.count(),  # lấy thật cho chuẩn
    }
    # nếu file của bạn nằm: templates/dashboard/dashboard.html
    return render(request, "dashboard/dashboard.html", context)
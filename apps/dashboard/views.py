import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .mock_data import (
    build_customers_data,
    orders_data,
    permissions_data,
    products_data,
)


def _format_currency(value):
    try:
        return f"{int(value):,}".replace(",", ".")
    except Exception:
        return "0"


def _get_product_or_none(product_id):
    try:
        product_id = int(product_id)
    except (TypeError, ValueError):
        return None
    return next((item for item in products_data if item["id"] == product_id), None)


def _get_order_or_none(order_id):
    return next((item for item in orders_data if item["id"] == order_id), None)


@login_required(login_url="core:login")
def dashboard_view(request):
    total_revenue = sum(order["total_price"] for order in orders_data)
    total_orders = len(orders_data)
    total_products = len(products_data)

    pending_orders = sum(1 for order in orders_data if order["status"] == "pending")
    processing_orders = sum(1 for order in orders_data if order["status"] == "processing")
    shipping_orders = sum(1 for order in orders_data if order["status"] == "shipping")
    completed_orders = sum(1 for order in orders_data if order["status"] == "completed")
    cancelled_orders = sum(1 for order in orders_data if order["status"] == "cancelled")

    context = {
        "stats": {
            "total_revenue": total_revenue,
            "total_revenue_display": _format_currency(total_revenue),
            "total_orders": total_orders,
            "total_products": total_products,
            "pending_orders": pending_orders,
            "processing_orders": processing_orders,
            "shipping_orders": shipping_orders,
            "completed_orders": completed_orders,
            "cancelled_orders": cancelled_orders,
        },
        "recent_orders": orders_data[:5],
    }
    return render(request, "dashboard/dashboard.html", context)


@login_required(login_url="core:login")
def report_view(request):
    revenue_labels = ["14/04", "15/04", "16/04", "17/04", "18/04", "19/04", "20/04"]
    revenue_values = [150000, 320000, 210000, 450000, 180000, 390000, 330000]
    order_values = [2, 4, 3, 5, 2, 4, 3]

    category_report = [
        {"name": "Đèn lồng", "value": 480000},
        {"name": "Hoa mai/đào", "value": 360000},
        {"name": "Bao lì xì", "value": 250000},
        {"name": "Dây trang trí", "value": 195000},
    ]

    top_products = [
        {"name": "Đèn lồng đỏ truyền thống", "quantity": 12, "revenue_display": "1.800.000"},
        {"name": "Bao lì xì hoa mai vàng", "quantity": 10, "revenue_display": "250.000"},
        {"name": "Cành hoa mai vàng", "quantity": 8, "revenue_display": "1.440.000"},
        {"name": "Dây treo trang trí Tết", "quantity": 5, "revenue_display": "225.000"},
    ]

    context = {
        "summary": {
            "revenue_display": _format_currency(sum(revenue_values)),
            "total_orders": sum(order_values),
            "avg_order_display": _format_currency(sum(revenue_values) // max(sum(order_values), 1)),
        },
        "revenue_chart_labels": json.dumps(revenue_labels, ensure_ascii=False),
        "revenue_chart_values": json.dumps(revenue_values),
        "order_chart_values": json.dumps(order_values),
        "category_report": category_report,
        "top_products": top_products,
    }
    return render(request, "dashboard/report.html", context)


@login_required(login_url="core:login")
def order_list_view(request):
    status = (request.GET.get("status") or "all").strip()
    keyword = (request.GET.get("q") or "").strip().lower()

    orders = list(orders_data)

    if status != "all":
        orders = [order for order in orders if order["status"] == status]

    if keyword:
        orders = [
            order
            for order in orders
            if keyword in order["id"].lower()
            or keyword in order["customer_name"].lower()
            or keyword in order["phone"].lower()
        ]

    context = {
        "orders": orders,
        "filters": {
            "status": status,
            "q": request.GET.get("q", ""),
        },
        "order_stats": {
            "all": len(orders_data),
            "pending": sum(1 for order in orders_data if order["status"] == "pending"),
            "processing": sum(1 for order in orders_data if order["status"] == "processing"),
            "shipping": sum(1 for order in orders_data if order["status"] == "shipping"),
            "completed": sum(1 for order in orders_data if order["status"] == "completed"),
            "cancelled": sum(1 for order in orders_data if order["status"] == "cancelled"),
        },
    }
    return render(request, "dashboard/orders.html", context)


@login_required(login_url="core:login")
def order_detail_view(request, order_id):
    order = _get_order_or_none(order_id)

    if not order:
        messages.error(request, "Không tìm thấy đơn hàng.")
        return redirect("dashboard:orders")

    return render(
        request,
        "dashboard/order_detail.html",
        {
            "order": order,
            "order_items": order["items"],
        },
    )


@login_required(login_url="core:login")
def product_list_view(request):
    keyword = (request.GET.get("q") or "").strip().lower()
    category = (request.GET.get("category") or "all").strip()
    status = (request.GET.get("status") or "all").strip()

    products = list(products_data)

    if keyword:
        products = [
            product
            for product in products
            if keyword in product["name"].lower()
            or keyword in product["category"].lower()
        ]

    if category != "all":
        products = [product for product in products if product["category"] == category]

    if status != "all":
        products = [product for product in products if product["status"] == status]

    categories = sorted({product["category"] for product in products_data})

    context = {
        "products": products,
        "categories": categories,
        "filters": {
            "q": request.GET.get("q", ""),
            "category": category,
            "status": status,
        },
    }
    return render(request, "dashboard/products.html", context)


@login_required(login_url="core:login")
def product_create_view(request):
    categories = sorted({product["category"] for product in products_data})

    if request.method == "POST":
        messages.success(request, "Đã lưu giao diện tạo sản phẩm.")
        return redirect("dashboard:products")

    context = {
        "categories": categories,
        "form_data": {
            "name": "",
            "price": "",
            "category": categories[0] if categories else "",
            "stock": "",
            "status": "active",
            "description": "",
        },
    }
    return render(request, "dashboard/product_create.html", context)


@login_required(login_url="core:login")
def product_edit_view(request, product_id):
    product = _get_product_or_none(product_id)

    if not product:
        messages.error(request, "Không tìm thấy sản phẩm.")
        return redirect("dashboard:products")

    categories = sorted({item["category"] for item in products_data})

    if request.method == "POST":
        messages.success(request, f"Đã cập nhật giao diện sản phẩm: {product['name']}.")
        return redirect("dashboard:products")

    return render(
        request,
        "dashboard/product_edit.html",
        {
            "product": product,
            "categories": categories,
        },
    )


@login_required(login_url="core:login")
def product_delete_view(request, product_id):
    product = _get_product_or_none(product_id)

    if not product:
        messages.error(request, "Không tìm thấy sản phẩm.")
        return redirect("dashboard:products")

    messages.success(request, f"Đã xử lý thao tác xóa cho sản phẩm: {product['name']}.")
    return redirect("dashboard:products")


@login_required(login_url="core:login")
def customer_list_view(request):
    customers = build_customers_data()

    keyword = (request.GET.get("q") or "").strip().lower()
    status = (request.GET.get("status") or "all").strip()
    sort = (request.GET.get("sort") or "newest").strip()

    if keyword:
        customers = [
            customer
            for customer in customers
            if keyword in customer["name"].lower()
            or keyword in customer["code"].lower()
            or keyword in customer["phone"].lower()
            or keyword in customer["email"].lower()
        ]

    if status != "all":
        customers = [customer for customer in customers if customer["status"] == status]

    if sort == "name_asc":
        customers.sort(key=lambda item: item["name"].lower())
    elif sort == "orders_desc":
        customers.sort(key=lambda item: item["order_count"], reverse=True)
    elif sort == "spent_desc":
        customers.sort(key=lambda item: item["total_spent"], reverse=True)

    all_customers = build_customers_data()

    context = {
        "customers": customers,
        "filters": {
            "q": request.GET.get("q", ""),
            "status": status,
            "sort": sort,
        },
        "customer_stats": {
            "all": len(all_customers),
            "active": sum(1 for customer in all_customers if customer["status"] == "active"),
            "new": sum(1 for customer in all_customers if customer["status"] == "new"),
            "vip": sum(1 for customer in all_customers if customer["status"] == "vip"),
            "inactive": sum(1 for customer in all_customers if customer["status"] == "inactive"),
        },
    }
    return render(request, "dashboard/customers.html", context)


@login_required(login_url="core:login")
def customer_create_view(request):
    if request.method == "POST":
        messages.success(request, "Đã lưu giao diện tạo khách hàng.")
        return redirect("dashboard:customers")

    return render(
        request,
        "dashboard/customer_create.html",
        {
            "form_data": {
                "name": "",
                "phone": "",
                "email": "",
                "city": "",
                "address": "",
                "status": "active",
                "note": "",
            }
        },
    )


@login_required(login_url="core:login")
def customer_detail_view(request, customer_id):
    customers = build_customers_data()
    customer = next((item for item in customers if item["id"] == customer_id), None)

    if not customer:
        messages.error(request, "Không tìm thấy khách hàng.")
        return redirect("dashboard:customers")

    customer_orders = [
        order for order in orders_data if order["customer_name"].lower() == customer["name"].lower()
    ]

    return render(
        request,
        "dashboard/customer_detail.html",
        {
            "customer": customer,
            "customer_orders": customer_orders,
        },
    )


@login_required(login_url="core:login")
def customer_lock_view(request, customer_id):
    customers = build_customers_data()
    customer = next((item for item in customers if item["id"] == customer_id), None)

    if not customer:
        messages.error(request, "Không tìm thấy khách hàng.")
        return redirect("dashboard:customers")

    if request.method == "POST":
        messages.success(request, f"Đã cập nhật trạng thái khóa cho khách hàng: {customer['name']}.")
        return redirect("dashboard:customer_detail", customer_id=customer_id)

    return render(
        request,
        "dashboard/customer_lock.html",
        {
            "customer": customer,
        },
    )


@login_required(login_url="core:login")
def permission_list_view(request):
    return render(request, "dashboard/permissions.html", {"permissions": permissions_data})
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Count
from products.models import Product
from orders.models import Order


@login_required(login_url='login')
def dashboard_view(request):
    orders = Order.objects.all().order_by('-created_at')
    recent_orders = list(orders[:5])

    completed_orders = Order.objects.filter(status='completed')

    total_orders = completed_orders.count()
    total_products = Product.objects.count()

    total_revenue = (
        completed_orders.aggregate(total=Sum('total_price'))['total'] or 0
    )

    formatted_revenue = f"{int(total_revenue):,}".replace(",", ".")

    for order in recent_orders:
        order.formatted_total_price = f"{int(order.total_price or 0):,}".replace(",", ".")

    count_new = orders.filter(status='new').count()
    count_processing = orders.filter(status='pending').count()
    count_shipping = orders.filter(status='shipping').count()
    count_completed = orders.filter(status='completed').count()
    count_cancelled = orders.filter(status='cancelled').count()

    context = {
        'formatted_revenue': formatted_revenue,
        'total_orders': total_orders,
        'total_products': total_products,
        'count_new': count_new,
        'count_processing': count_processing,
        'count_shipping': count_shipping,
        'count_completed': count_completed,
        'count_cancelled': count_cancelled,
        'recent_orders': recent_orders,
    }

    return render(request, 'dashboard/dashboard.html', context)

@login_required(login_url='login')
def report_view(request):
    orders = Order.objects.all()

    # chỉ tính đơn thành công
    completed_orders = orders.filter(status='completed')

    total_orders = completed_orders.count()

    total_revenue = completed_orders.aggregate(
        total=Sum('total_price')
    )['total'] or 0

    formatted_revenue = f"{int(total_revenue):,}".replace(",", ".")

    # tỷ lệ huỷ
    total_all = orders.count()
    total_cancelled = orders.filter(status='cancelled').count()

    cancel_rate = 0
    if total_all > 0:
        cancel_rate = round((total_cancelled / total_all) * 100, 1)

    context = {
        'total_revenue': formatted_revenue,
        'total_orders': total_orders,
        'cancel_rate': cancel_rate,
    }

    return render(request, 'dashboard/report.html', context)


@login_required(login_url='login')
def order_list_view(request):
    orders = Order.objects.select_related('user').all().order_by('-created_at')

    context = {
        'orders': orders
    }
    return render(request, 'dashboard/orders.html', context)


@login_required(login_url='login')
def order_detail_view(request, order_id):
    order = get_object_or_404(Order.objects.select_related('user'), id=order_id)

    if request.method == "POST":
        new_status = request.POST.get("status")

        valid_transitions = {
            'new': ['pending', 'cancelled'],
            'pending': ['shipping', 'cancelled'],
            'shipping': ['completed'],
            'completed': [],
            'cancelled': [],
        }
        print("METHOD:", request.method)
        print("CURRENT:", order.status)
        print("POST STATUS:", request.POST.get("status"))
        if new_status and new_status in valid_transitions.get(order.status, []):
            order.status = new_status
            order.save()

        return redirect('order_detail', order_id=order.id)

    context = {
        'order': order
    }
    return render(request, 'dashboard/order_detail.html', context)

def product_list_view(request):
    products = Product.objects.all().order_by("-id")
    return render(request, "dashboard/products.html", {"products": products})


def product_create_view(request):
    return render(request, "dashboard/product_create.html")


def product_update_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "dashboard/product_edit.html", {"product": product})


def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect("product_list")

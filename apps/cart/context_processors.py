# apps/cart/context_processors.py

from .utils import get_cart_total_quantity


def cart_badge(request):
    return {
        "cart_total_quantity": get_cart_total_quantity(request)
    }
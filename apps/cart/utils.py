# apps/cart/utils.py

CART_SESSION_KEY = "cart"


def price_to_int(value):
    try:
        return int(str(value).replace(".", "").replace(",", "").replace("đ", "").strip())
    except (TypeError, ValueError):
        return 0


def format_currency(value):
    try:
        return f"{int(value):,}".replace(",", ".")
    except (TypeError, ValueError):
        return "0"


def get_product_by_id(product_id):
    from apps.core.views import products_data

    return next((p for p in products_data if p["id"] == int(product_id)), None)


def get_cart(request):
    cart = request.session.get(CART_SESSION_KEY, {})

    if not isinstance(cart, dict):
        cart = {}
        request.session[CART_SESSION_KEY] = cart
        request.session.modified = True

    return cart


def save_cart(request, cart):
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True


def get_cart_total_quantity(request):
    cart = get_cart(request)
    total = 0

    for qty in cart.values():
        try:
            total += int(qty)
        except (TypeError, ValueError):
            pass

    return total


def build_cart_context(request):
    cart = get_cart(request)

    items = []
    total_quantity = 0
    total_price = 0
    cleaned_cart = {}

    for product_id, quantity in cart.items():
        try:
            product_id_int = int(product_id)
            quantity_int = max(1, int(quantity))
        except (TypeError, ValueError):
            continue

        product = get_product_by_id(product_id_int)
        if not product:
            continue

        price_int = price_to_int(product.get("price"))
        subtotal_int = price_int * quantity_int

        items.append({
            "id": product_id_int,
            "name": product.get("name"),
            "image": product.get("image"),
            "category": product.get("category"),
            "price": price_int,
            "price_display": format_currency(price_int),
            "quantity": quantity_int,
            "subtotal": subtotal_int,
            "subtotal_display": format_currency(subtotal_int),
        })

        cleaned_cart[str(product_id_int)] = quantity_int
        total_quantity += quantity_int
        total_price += subtotal_int

    if cleaned_cart != cart:
        save_cart(request, cleaned_cart)

    return {
        "items": items,
        "total_quantity": total_quantity,
        "total_price": total_price,
        "total_price_display": format_currency(total_price),
    }
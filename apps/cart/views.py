from django.shortcuts import render



def cart_detail(request):
    
    return render(request, "cart/detail.html")

def add(request, product_id):
    # lấy cart trong session
    cart = request.session.get("cart", {})

    product_id = str(product_id)

    # nếu đã có thì tăng số lượng
    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session["cart"] = cart

    return redirect("cart:detail")

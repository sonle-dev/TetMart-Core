from django.urls import path

from .views import (
    account_view,
    cancel_order_view,
    index,
    login_view,
    logout_view,
    my_orders_view,
    product_detail,
    product_list_view as public_product_list_view,
    register_view,
    reorder_order_view,
)

app_name = "core"

urlpatterns = [
    path("", index, name="home"),
    path("products/", public_product_list_view, name="product_list"),
    path("product-detail/<int:product_id>/", product_detail, name="product_detail"),
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path("account/", account_view, name="account"),
    path("my-orders/", my_orders_view, name="my_orders"),
    path("my-orders/reorder/<str:order_id>/", reorder_order_view, name="reorder_order"),
    path("my-orders/cancel/<str:order_id>/", cancel_order_view, name="cancel_order"),
]
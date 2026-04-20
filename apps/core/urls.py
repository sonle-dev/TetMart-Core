from django.urls import path

from .views import (
    index,
    login_view,
    logout_view,
    product_detail,
    product_list_view as public_product_list_view,
    register_view,
)

app_name = "core"

urlpatterns = [
    path("", index, name="home"),
    path("products/", public_product_list_view, name="product_list"),
    path("product-detail/<int:product_id>/", product_detail, name="product_detail"),
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
]
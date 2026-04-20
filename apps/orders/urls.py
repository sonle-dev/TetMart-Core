from django.urls import path

from .views import (
    bank_transfer_view,
    checkout_view,
    confirm_bank_transfer_view,
    order_success_view,
)

app_name = "orders"

urlpatterns = [
    path("checkout/", checkout_view, name="checkout"),
    path("bank-transfer/", bank_transfer_view, name="bank_transfer"),
    path("bank-transfer/confirm/", confirm_bank_transfer_view, name="confirm_bank_transfer"),
    path("success/", order_success_view, name="success"),
]
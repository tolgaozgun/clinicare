from cart.views import ShoppingCartView
from django.urls import path

app_name = "cart"

urlpatterns = [
    path("", ShoppingCartView.as_view(), name="cart"),
]
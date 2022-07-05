from accounts.models import User
from django.db import models

from panel.models import Product


class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="cart_customer")
    lastUpdated = models.DateTimeField(auto_now=True)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, default=None, related_name="cart_products_cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None, related_name="cart_products_product")
    quantity = models.SmallIntegerField()



from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from djmoney.models.fields import MoneyField
from accounts.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='TRY')
    coverImage = models.ForeignKey("ProductImage", blank=True, null=True, on_delete=models.CASCADE, related_name="product_cover_image")
    dateCreated = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now=True)


class OrderProduct(Product):
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    dateAdded = models.DateTimeField(auto_now_add=True)


class ProductImage(models.Model):
    file = models.ImageField(upload_to="product", default="product/default.png")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image_product")


class Order(models.Model):
    orderNo = models.CharField(max_length=40)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name="order_customer")
    products = models.ManyToManyField(Product)
    lastUpdated = models.DateTimeField(auto_now=True)
    billing = models.ForeignKey('Billing', on_delete=models.CASCADE, default=None, related_name="order_billing")
    dateCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart: " + str(id)


class Billing(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=None, related_name="billing_order")
    paymentMethod = models.SmallIntegerField(default=1) # Enum
    isPaid = models.BooleanField(default=False)
    dateCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Billing: " + str(id)
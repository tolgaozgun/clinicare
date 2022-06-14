from django.contrib import admin
from .models import Report, Prescription, Appointment, Product, OrderProduct, Order, Billing, Cart

admin.site.register(Report)
admin.site.register(Prescription)
admin.site.register(Appointment)
admin.site.register(Product)
admin.site.register(OrderProduct)
admin.site.register(Order)
admin.site.register(Billing)
admin.site.register(Cart)

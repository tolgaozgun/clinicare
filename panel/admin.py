from django.contrib import admin

# Register your models here.


from .models import User, Report, Prescription, Appointment, Product, OrderProduct, Order

admin.site.register(User)
admin.site.register(Report)
admin.site.register(Prescription)
admin.site.register(Appointment)
admin.site.register(Product)
admin.site.register(OrderProduct)
admin.site.register(Order)

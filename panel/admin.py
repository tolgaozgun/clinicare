from django.contrib import admin

# Register your models here.


from .models import User, Report, Prescription

admin.site.register(User)
admin.site.register(Report)
admin.site.register(Prescription)

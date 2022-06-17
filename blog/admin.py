from blog.models import BlogCategory, BlogPost
from django.contrib import admin

# Register your models here.

admin.site.register(BlogPost)
admin.site.register(BlogCategory)
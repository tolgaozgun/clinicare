from accounts.models import User
from django.db import models


class BlogPost(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    text = models.TextField()
    dateCreated = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="blog", default="blog/default.png")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogpost_author")
    related_posts = models.ManyToManyField("BlogPost")
    word_list = models.TextField()
    similarity = models.TextField()


class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    dateCreated = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="blog", default="blog/default.png")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogcategory_creator", null=True, blank=True)
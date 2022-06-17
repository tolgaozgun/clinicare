from blog.views import IndexView, PostView
from django.urls import path

app_name = "blog"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("posts", IndexView.as_view(), name="posts"),
    path("posts/<int:pk>", PostView.as_view(), name="post"),
]
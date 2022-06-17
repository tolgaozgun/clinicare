from blog.views import IndexView, PostView, AddPostView, DeletePostView, EditPostView
from django.urls import path

app_name = "blog"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("posts", IndexView.as_view(), name="posts"),
    path("posts/new", AddPostView.as_view(), name="add_post"),
    path("posts/<int:pk>", PostView.as_view(), name="post"),
    path("posts/<int:pk>/edit", EditPostView.as_view(), name="edit_post"),
    path("posts/<int:pk>/delete", DeletePostView.as_view(), name="delete_post"),
]
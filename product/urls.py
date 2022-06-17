from django.urls import path
from .views import ProductsView, ProductView, AddProductView, DeleteProductView, EditProductView

app_name = "product"

urlpatterns = [
    path("", ProductsView.as_view(), name="products"),
    path("new", AddProductView.as_view(), name="add_product"),
    path("<int:pk>", ProductView.as_view(), name="product"),
    path("<int:pk>/edit", EditProductView.as_view(), name="edit_product"),
    path("<int:pk>/delete", DeleteProductView.as_view(), name="delete_product"),
]
from django.urls import path
from .views import (
    catalog,
    product,
    add_to_cart,
    cart_detail,
    order_create,
    remove_from_cart,
)

app_name = "goods"

urlpatterns = [
    path("", catalog, name="index"),
    path("product/<slug:slug>/", product, name="product"),
    path("add-to-cart/", add_to_cart, name="add_to_cart"),
    path("cart/", cart_detail, name="cart_detail"),
    path("order/", order_create, name="order_create"),
    path(
        "remove_from_cart/<int:product_id>/", remove_from_cart, name="remove_from_cart"
    ),
]

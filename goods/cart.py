from decimal import Decimal
from django.conf import settings
from goods.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart

    def add(self, product_id, quantity=1, override_quantity=False):
        product_id = str(product_id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0}
        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            item = self.cart[str(product.id)]
            item["product"] = product
            item["total_price"] = product.price * item["quantity"]
            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            item["quantity"] * Product.objects.get(id=pid).price
            for pid, item in self.cart.items()
        )

    def clear(self):
        self.session["cart"] = {}
        self.save()

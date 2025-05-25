from .cart import Cart


def cart_counter(request):
    return {"cart_item_count": len(Cart(request))}

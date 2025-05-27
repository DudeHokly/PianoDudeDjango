from django.shortcuts import get_object_or_404, render, redirect
from datetime import datetime
from django.core.paginator import Paginator

from django.http import JsonResponse

from goods.cart import Cart
from goods.models import Product


def get_menu():
    return [
        {
            "label": {"name": "Каталог", "path": "/catalog"},
            "links": [
                {"name": "Мелодии", "path": "/catalog"},
                {"name": "Ритмы", "path": "/catalog"},
                {"name": "Гармонии", "path": "/catalog"},
                {"name": "Вдохновение", "path": "/catalog"},
                {"name": "Симфония", "path": "/catalog"},
            ],
        },
        {
            "label": {"name": "Контакты", "path": "/contacts"},
            "links": [
                {"name": "Обратная связь", "path": "/contacts"},
            ],
        },
    ]


def get_footer_links():
    return {
        "Информация": [
            "Главная",
            "Преимущества",
            "Отзывы",
            "Доставка",
            "Оплата",
            "Контакты",
            "Статьи",
        ],
        "Клиентам": [
            "Как заказать",
            "Рассрочка",
            "Кредит",
            "Гарантия",
            "Условия возврата",
            "Сервис",
            "О нас",
        ],
        "Каталог": ["Клавишные", "Караоке", "Звук", "Дисконт", "Оплата"],
    }


# Create your views here.
def catalog(request):
    sort = request.GET.get("sort", "")
    price = request.GET.get("price", "")
    manufacturer = request.GET.getlist("Производитель")
    color = request.GET.getlist("Цвет")

    products = Product.objects.all()

    if color:
        products = products.filter(color__in=color)
    if manufacturer:
        products = products.filter(manufacturer__in=manufacturer)
    if price:
        try:
            products = products.filter(price__gte=float(price))
        except ValueError:
            pass

    if sort == "price_asc":
        products = products.order_by("price")
    elif sort == "price_desc":
        products = products.order_by("-price")
    elif sort == "name":
        products = products.order_by("name")

    paginator = Paginator(products, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    filters = {
        "Цвет": Product.objects.values_list("color", flat=True).distinct(),
        "Производитель": Product.objects.values_list(
            "manufacturer", flat=True
        ).distinct(),
        "Полифония": ["16", "32", "48", "64", "80", "128", "256"],
        "Количество клавиш": ["61", "68", "73", "76", "88"],
        "Метроном": ["Есть", "Нет", "Да"],
        "Устройство записи": ["Есть", "Нет", "Да"],
        "Bluetooth": ["Да", "Нет"],
        "Кол-во тембров": ["1", "2", "3", "10", "20", "50", "100+"],
        "Молоточковая": ["Да", "Нет"],
        "Вид питания": ["Внешний источник питания", "От сети 220В"],
        "Гарантийный срок": ["12 месяцев"],
        "Звуковые эффекты": ["Chorus", "Reverb", "Equalizer", "Phaser", "Flanger"],
        "Функции": [
            "Запись песен",
            "Метроном",
            "Транспонирование",
            "Аккомпанемент",
            "Арпеджиатор",
        ],
        "Жесткость клавиатуры": ["Взвешенная", "Невзвешенная", "Полувзвешенная"],
        "Размер клавиш": ["Полуразмерная", "Полноразмерная"],
        "Интерфейсы": ["6,3 мм", "3,5 мм", "USB", "AUX"],
    }

    selected_filters = {}
    for filter_name in filters.keys():
        selected_filters[filter_name] = request.GET.getlist(filter_name)

    full_context = {
        "menu_items": get_menu(),
        "products": page_obj,
        "filters": filters,
        "selected_filters": selected_filters,
        "footer_links": get_footer_links(),
        "year": datetime.now().year,
        "selected_sort": sort,
        "selected_color": color,
        "selected_manufacturer": manufacturer,
        "selected_price": price,
    }

    partial_context = {
        "products": page_obj,
        "filters": filters,
        "selected_filters": selected_filters,
        "selected_sort": sort,
        "selected_color": color,
        "selected_manufacturer": manufacturer,
        "selected_price": price,
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, "catalog_products.html", partial_context)
    else:
        return render(request, "catalog.html", full_context)


def product(request, slug):
    product = get_object_or_404(Product, slug=slug)

    return render(
        request,
        "product.html",
        {
            "menu_items": get_menu(),
            "product": product,
            "footer_links": get_footer_links(),
            "year": datetime.now().year,
        },
    )


def add_to_cart(request):
    if (
        request.method == "POST"
        and request.headers.get("x-requested-with") == "XMLHttpRequest"
    ):
        product_id = request.POST.get("product_id")
        if not product_id:
            return JsonResponse({"success": False, "message": "No product ID"})

        cart = Cart(request)
        cart.add(product_id)
        return JsonResponse({"success": True, "cart_count": len(cart)})

    return JsonResponse({"success": False, "message": "Invalid request"})


def cart_detail(request):
    cart = Cart(request)
    return render(
        request,
        "cart_detail.html",
        {
            "cart": cart,
            "menu_items": get_menu(),
            "footer_links": get_footer_links(),
            "year": datetime.now().year,
        },
    )


def order_create(request):
    return render(
        request,
        "order_create.html",
        {
            "menu_items": get_menu(),
            "footer_links": get_footer_links(),
            "year": datetime.now().year,
        },
    )


def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session["cart"] = cart
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"success": True})
    return redirect("goods:cart_detail")

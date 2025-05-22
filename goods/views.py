from django.shortcuts import get_object_or_404, render
from datetime import datetime
from django.core.paginator import Paginator

from goods.models import Product


def get_menu():
    return [
        {
            "label": {"name": "Каталог", "path": "/catalog"},
            "links": [
                {"name": "Гитары", "path": "/catalog"},
                {"name": "Клавишные", "path": "/catalog"},
                {"name": "Ударные", "path": "/catalog"},
                {"name": "Смычковые", "path": "/catalog"},
                {"name": "Электроника", "path": "/catalog"},
            ],
        },
        {
            "label": {"name": "Услуги", "path": "/FakeReviews"},
            "links": [
                {"name": "Ремонт инструментов", "path": "/Maintenance"},
                {"name": "Обучение игре", "path": "/TeachingPage"},
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
    sort = request.GET.get("sort")
    products = Product.objects.all()

    color = request.GET.getlist("Цвет")
    manufacturer = request.GET.getlist("Производитель")
    price = request.GET.get("price")

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
        "Записывающее устройство": ["Есть", "Нет", "Да"],
        "Bluetooth": ["Да", "Нет"],
        "Кол-во тембров": ["1", "2", "3", "10", "20", "50", "100+"],
        "Молоточковая клавиатура": ["Да", "Нет"],
        "Размеры, мм": ["1326 х 272 х 129 мм", "Компактные", "Стандартные", "Большие"],
        "Вес товара, г": ["11500", "70000", "45000", "13800", "17100"],
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

    return render(
        request,
        "catalog.html",
        {
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
        },
    )


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

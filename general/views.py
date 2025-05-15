from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth import logout, login

from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.models import User

# signals.py (автосоздание профиля)
from django.db.models.signals import post_save
from django.dispatch import receiver

from general.models import UserProfile

from .forms import RegisterForm


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
                {"name": "Обратная связь", "path": "/feedback"},
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


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("general:index")
    else:
        form = AuthenticationForm()

    return render(
        request,
        "login.html",
        {
            "form": form,
            "menu_items": get_menu(),
            "footer_links": get_footer_links(),
            "year": datetime.now().year,
        },
    )


def logout_view(request):
    logout(request)
    return redirect("general:index")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = RegisterForm()

    return render(
        request,
        "register.html",
        {
            "menu_items": get_menu(),
            "form": form,
            "footer_links": get_footer_links(),
            "year": datetime.now().year,
        },
    )


# @staff_member_required
def panel_admin(request):
    # Здесь будет логика:
    # - Сбор статистики посещений
    # - История заказов
    # - Обработка заказов
    # Пока заглушка:
    return render(request, "panel_admin.html")


def index(request):
    slogans = [
        {
            "icon": "biceps-flexed",
            "title": "Музыка для души и вдохновения",
            "text_below": "Создавайте мелодии, которые трогают сердца.",
        },
        {
            "icon": "sparkles",
            "title": "Ощути магию каждого аккорда",
            "text_below": "Музыкальные инструменты для настоящих творцов.",
        },
        {
            "icon": "file-music",
            "title": "Звук, который оживляет мечты",
            "text_below": "Откройте мир музыки вместе с нами.",
        },
    ]

    items = [
        {
            "icon": "cigarette",
            "title": "Мелодия вашей мечты",
            "description": "Откройте мир звуков с нашими инструментами.",
        },
        {
            "icon": "ear",
            "title": "Звуки, рождающие эмоции",
            "description": "Создавайте музыку с лучшими инструментами.",
        },
        {
            "icon": "cat",
            "title": "Гармония в каждой ноте",
            "description": "Выберите инструмент своей мечты у нас.",
        },
    ]

    carousel_slider = [
        {"image_url": "static/dependencies/images/mainPage/cube1.jpg"},
        {"image_url": "static/dependencies/images/mainPage/mainPage1.png"},
        {"image_url": "static/dependencies/images/mainPage/mainPage1.png"},
    ]

    news = [
        {
            "id": 1,
            "title": "Грандиозная распродажа гитар",
            "text": "Скидки до 30% на электрогитары весь июнь!",
            "background_Image": "dependencies/images/mainPage/newsLenta/adNews1.jpg",
        },
        {
            "id": 2,
            "title": "Мастер-класс от виртуоза",
            "text": "Известный пианист проведет бесплатный урок!",
            "background_Image": "dependencies/images/mainPage/newsLenta/adNews2.jpg",
        },
        {
            "id": 3,
            "title": "Новинка: цифровые пианино Yamaha",
            "text": "Поступление моделей с расширенным функционалом.",
            "background_Image": "dependencies/images/mainPage/newsLenta/adNews3.jpg",
        },
        {
            "id": 4,
            "title": "Конкурс молодых талантов",
            "text": "Участвуйте и выиграйте профессиональный микрофон!",
            "background_Image": "dependencies/images/mainPage/newsLenta/adNews4.jpg",
        },
        {
            "id": 5,
            "title": "Специальное предложение для школ",
            "text": "Комплекты музыкальных инструментов со скидкой 20%.",
            "background_Image": "dependencies/images/mainPage/newsLenta/adNews5.jpg",
        },
        {
            "id": 6,
            "title": "Отдел винтажных инструментов",
            "text": "Редкие экземпляры теперь в нашем магазине.",
            "background_Image": "dependencies/images/mainPage/newsLenta/adNews6.jpg",
        },
        {
            "id": 7,
            "title": "Бесплатная доставка по всей стране",
            "text": "От 10000 рублей доставим ваш инструмент бесплатно!",
            "background_Image": "dependencies/images/mainPage/newsLenta/adNews7.jpg",
        },
    ]

    return render(
        request,
        "index.html",
        {
            "menu_items": get_menu(),
            "slogans": slogans,
            "items": items,
            "carousel_slider": carousel_slider,
            "news": news,
            "footer_links": get_footer_links(),
            "year": datetime.now().year,
        },
    )


def account(request):
    purchased_products = [
        {
            "name": "Электропианино Yamaha P-45",
            "description": "Отличное цифровое пианино для начинающих и продвинутых музыкантов.",
            "price": "42 990",
            "old_price": "47 990",
        },
        # другие товары...
    ]

    return render(
        request,
        "account.html",
        {
            "menu_items": get_menu(),
            "purchased_products": purchased_products,
            "footer_links": get_footer_links(),
            "year": datetime.now().year,
        },
    )


def contacts(request):
    employees = [
        {
            "srcImg": "dependencies/images/contacts/emplyee1.jpg",
            "employeeName": "Алексей Иванов",
            "employeePosition": "Менеджер по продажам",
        },
        {
            "srcImg": "dependencies/images/contacts/emplyee2.jpg",
            "employeeName": "Дмитрий Кузнецов",
            "employeePosition": "Технический консультант",
        },
        {
            "srcImg": "dependencies/images/contacts/giga1.jpg",
            "employeeName": "Алексей Сергеевич",
            "employeePosition": "Глава компании",
        },
    ]

    return render(
        request,
        "contacts.html",
        {
            "menu_items": get_menu(),
            "employees": employees,
            "footer_links": get_footer_links(),
            "year": datetime.now().year,
        },
    )


def feedback(request):
    return render(
        request,
        "feedback.html",
        {
            "menu_items": get_menu(),
            "footer_links": get_footer_links(),
            "year": datetime.now().year,
        },
    )

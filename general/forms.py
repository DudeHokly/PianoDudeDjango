from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from django.db import transaction

from general.models import UserProfile

tailwind_input_classes = "mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-[#008080] focus:border-[#008080]"


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Логин",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": tailwind_input_classes,
                "placeholder": "Введите логин",
                "required": "required",
            }
        ),
    )
    fio = forms.CharField(
        label="ФИО",
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": tailwind_input_classes,
                "placeholder": "Введите ФИО",
                "required": "required",
            }
        ),
    )
    phone = forms.CharField(
        label="Телефон",
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "class": tailwind_input_classes,
                "placeholder": "Введите телефон",
                "required": "required",
            }
        ),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": tailwind_input_classes,
                "placeholder": "Введите email",
                "required": "required",
            }
        ),
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={
                "class": tailwind_input_classes,
                "placeholder": "Введите пароль",
                "required": "required",
            }
        ),
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(
            attrs={
                "class": tailwind_input_classes,
                "placeholder": "Повторите пароль",
                "required": "required",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["username", "fio", "phone", "email", "password1", "password2"]

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким логином уже существует.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Пользователь с таким email уже зарегистрирован."
            )
        return email

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if UserProfile.objects.filter(phone=phone).exists():
            raise forms.ValidationError(
                "Пользователь с таким номером телефона уже зарегистрирован."
            )
        return phone

    def save(self, commit=True):
        with transaction.atomic():
            user = super().save(commit=False)
            user.email = self.cleaned_data["email"]
            if commit:
                user.save()
                UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        "fio": self.cleaned_data["fio"],
                        "phone": self.cleaned_data["phone"],
                    },
                )
            return user

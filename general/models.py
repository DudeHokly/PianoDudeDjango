from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fio = models.CharField("ФИО", max_length=255)
    phone = models.CharField("Телефон", max_length=20)

    def __str__(self):
        return self.user.username

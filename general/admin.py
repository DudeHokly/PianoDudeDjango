from django.contrib import admin

from general.models import UserProfile
from goods.models import Product

# Register your models here.
admin.site.register(Product)
admin.site.register(UserProfile)

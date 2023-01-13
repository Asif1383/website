from django.contrib import admin
from .models import MyUser, Product, CartItem, MultipleProduct
# Register your models here.
admin.site.register(Product)
admin.site.register((MyUser, CartItem, MultipleProduct))




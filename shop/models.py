from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from . import Managers
from django.contrib.auth.models import PermissionsMixin


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    discount_price = models.FloatField()
    category = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField()
    cart_to_product = models.ManyToManyField('CartItem', blank=True)


class CartItem(models.Model):
    cart_id = models.IntegerField(primary_key=True,)
    cart_to_user = models.OneToOneField('MyUser', on_delete=models.CASCADE)


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    is_staff = models.BooleanField(default=False)
    objects = Managers.MyUserManager()


class MultipleProduct(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user = models.ForeignKey('MyUser', on_delete=models.CASCADE)
    total_product = models.IntegerField(default=0)

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    male = models.BooleanField(default = False)
    enabled = models.BooleanField(default = True)
    BoundPayment = models.CharField(max_length = 32, default = "none")

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length = 256)

    def __str__(self):
        return self.name

class Product(models.Model):
    seller = models.ForeignKey(Profile,on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null = True, on_delete = models.SET_NULL)
    uid = models.IntegerField(default = 0, unique = True)
    price = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)
    name = models.CharField(max_length = 32)
    description = models.TextField(default = "暂无说明")
    state = models.IntegerField(default = 0)

    def __str__(self):
        return self.name

class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    descripition = models.CharField(max_length = 32, default = "商品照片")
    url = models.URLField(default = "/static/images/no_image")

    def __str__(self):
        return self.description

class Order(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    full_name = models.CharField(max_length = 32)
    address = models.CharField(max_length = 256)
    phone = models.CharField(max_length = 15)
    created_at = models.DateTimeField(auto_now_add = True)
    update_at = models.DateTimeField(auto_now = True)
    paid = models.BooleanField(default = False)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return 'Order:{}'.format(self.id)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE, related_name = 'items')
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)

    def __str__(self):
        return '{}'.format(self.id)
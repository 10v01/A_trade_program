from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    male = models.BooleanField(default = False)
    enabled = models.BooleanField(default = True)
    full_name = models.CharField(max_length = 32, null = True, blank = True)
    phone = models.CharField(max_length = 15, null = True, blank = True)
    address = models.CharField(max_length = 256, null = True, blank = True)
    BoundPayment = models.CharField(max_length = 32, null = True, blank = True)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length = 256)

    def __str__(self):
        return self.name

class Product(models.Model):
    seller = models.ForeignKey(Profile,on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null = True, blank = True, on_delete = models.SET_NULL)
    price = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)
    name = models.CharField(max_length = 32)
    description = models.TextField(default = "暂无说明")
    state = models.IntegerField(default = 0)#0代表待售，1代表已有人提交订单

    def __str__(self):
        return self.name

class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    descripition = models.CharField(max_length = 32, default = "商品照片")
    url = models.URLField(default = "/static/images/no_image")

    def __str__(self):
        return self.description

class Order(models.Model):
    buyer = models.ForeignKey(Profile, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    price = models.IntegerField()
    full_name = models.CharField(max_length = 32)
    address = models.CharField(max_length = 256)
    phone = models.CharField(max_length = 15)
    created_at = models.DateTimeField(auto_now_add = True)
    update_at = models.DateTimeField(auto_now = True)
    state = models.IntegerField(default = 0)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return 'Order:{}'.format(self.id)

class Mark(models.Model):
    marker = models.ForeignKey(Profile, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)

    def __str__(self):
        return 'Mark:{}'.format(self.id)
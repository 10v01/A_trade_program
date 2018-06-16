from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.IntegerField(default = 0)
    #0代表保密，1代表男，2代表女
    enabled = models.BooleanField(default=False)
    full_name = models.CharField(max_length=32, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    BoundPayment = models.CharField(max_length=32, null=True, blank=True)
    usertype = models.IntegerField(default=0)
    email = models.EmailField(null=True, blank=True)
    email_binding = models.EmailField(null=True, blank=True)
    email_binding_key = models.CharField(max_length=4, null=True, blank=True)
    pay_binding = models.CharField(max_length=32, null=True, blank=True)
    pay_binding_key = models.CharField(max_length=4, null=True, blank=True)

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
    state = models.IntegerField(default = -1)
    #0代表待售，1代表已有人提交订单，2代表已付款， 3代表已发货， 4代表已签收， -1代表商品正在等待审核，-2代表审核不通过

    def __str__(self):
        return self.name

class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    descripition = models.CharField(max_length = 32, default = "商品照片")
    url = models.URLField(default = "/static/images/no_image")

    def __str__(self):
        return self.product.name + "/" + self.description

class Order(models.Model):
    buyer = models.ForeignKey(Profile, on_delete = models.CASCADE)
    product = models.OneToOneField(Product, on_delete = models.CASCADE)
    price = models.IntegerField()
    full_name = models.CharField(max_length = 32)
    address = models.CharField(max_length = 256)
    phone = models.CharField(max_length = 15)
    created_at = models.DateTimeField(auto_now_add = True)
    state = models.IntegerField(default = 0)
    # 0:初始状态，1:支付平台生成订单，2:已付款，3:已发货，4:已收货，5:已评价，-1:已取消
    payment_id = models.IntegerField(null = True, blank = True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return 'Order:{}'.format(self.id)

class Mark(models.Model):
    marker = models.ForeignKey(Profile, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)

    def __str__(self):
        return 'Mark:{}'.format(self.id)

class Comment(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    stars = models.IntegerField()
    comment_text = models.CharField(max_length = 512, null = True, blank = True)

    def __str__(self):
        return 'Comment:{}'.format(self.id)
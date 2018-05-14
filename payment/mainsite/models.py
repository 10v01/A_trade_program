from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    paypassword = models.CharField(max_length = 32)

    def __str__(self):
        return self.user.username

class Payment(models.Model):
    payer = models.ForeignKey(Profile, related_name="payer", on_delete = models.CASCADE)
    receiver = models.ForeignKey(Profile, related_name="receiver", on_delete = models.CASCADE)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)
    order = models.IntegerField()
    state = models.IntegerField(default = 0)

    def __str__(self):
        return 'Payment:{}'.format(self.id)

class Binding(models.Model):
    profile = models.ForeignKey(Profile, on_delete = models.CASCADE)
    trade_profile = models.CharField(max_length = 256)
    key = models.CharField(max_length = 16)

    def __str__(self):
        return 'Profile:{}, id:{}'.format(self.profile.user.username, self.id)

class EmailBinding(models.Model):
    email = models.EmailField(unique=True)
    key = models.CharField(max_length = 4)

    def __str__(self):
        return self.email
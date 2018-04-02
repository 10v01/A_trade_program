from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    male = models.BooleanField(default = False)
    usertype = models.IntegerField(default = 0)
    enabled = models.BooleanField(default = True)

    def __str__(self):
        return self.user.username

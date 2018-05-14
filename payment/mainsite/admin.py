from django.contrib import admin
from mainsite import models

# Register your models here.

admin.site.register(models.Profile)
admin.site.register(models.Payment)
admin.site.register(models.Binding)
admin.site.register(models.EmailBinding)
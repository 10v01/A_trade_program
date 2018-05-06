from django.contrib import admin
from mainsite import models

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "uid", "category", "price", "seller")
    ordering = ("uid",)

admin.site.register(models.Profile)
admin.site.register(models.Category)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductPhoto)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)

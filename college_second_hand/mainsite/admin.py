from django.contrib import admin
from mainsite import models

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "id")
    ordering = ("id",)

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "category", "price", "seller")
    ordering = ("id",)

admin.site.register(models.Profile)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductPhoto)
admin.site.register(models.Order)

from django.contrib import admin
from mainsite import models

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "id")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "id")
    ordering = ("id",)

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "category", "price", "seller")
    ordering = ("id",)

class OrderAdmin(admin.ModelAdmin):
    list_display = ("buyer", "product", "price", "created_at", "update_at")

admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Order)
admin.site.register(models.Mark)
admin.site.register(models.Comment)

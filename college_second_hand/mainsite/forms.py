#-*- coding:utf-8 -*-
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label = '用户名', max_length = 16)
    password = forms.CharField(label = '密码', widget = forms.PasswordInput(), max_length = 32)

class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', max_length = 16)
    password = forms.CharField(label = '密码', widget = forms.PasswordInput(), max_length = 32)
    confirm_password = forms.CharField(label = '确认密码', widget = forms.PasswordInput(), max_length = 32)

class CartAddForm(forms.Form):
    product_id = forms.IntegerField()

class ProductForm(forms.Form):
    category = forms.IntegerField(label='category', min_value = 1, max_value = 3)
    price = forms.DecimalField(max_digits=10, decimal_places=2, min_value = 0, max_value = 99999999.99)
    name = forms.CharField(max_length = 32)

class ProductDescriptionForm(forms.Form):
    description = forms.CharField(max_length=256)

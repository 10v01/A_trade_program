#-*- coding:utf-8 -*-
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label = '用户名', max_length = 16)
    password = forms.CharField(label = '密码', widget = forms.PasswordInput(), max_length = 32)

class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', max_length = 16)
    password = forms.CharField(label = '密码', widget = forms.PasswordInput(), max_length = 32)
    confirm_password = forms.CharField(label = '确认密码', widget = forms.PasswordInput(), max_length = 32)

class OrderAddForm(forms.Form):
    product_id = forms.IntegerField()

class OrderIDForm(forms.Form):
    order_id = forms.IntegerField()

class MarkAddForm(forms.Form):
    product_id = forms.IntegerField()

class MarkRemoveForm(forms.Form):
    mark_id = forms.IntegerField()

class ProductForm(forms.Form):
    category = forms.IntegerField(label='category', min_value = 1, max_value = 3)
    price = forms.DecimalField(max_digits=10, decimal_places=2, min_value = 0, max_value = 99999999.99)
    name = forms.CharField(max_length = 32)

class ProfileModifyForm(forms.Form):
    sex = forms.IntegerField(min_value = 0, max_value = 2)
    full_name = forms.CharField(max_length = 32)
    phone = forms.CharField(max_length = 15)
    address = forms.CharField(max_length = 256)

class ProductDescriptionForm(forms.Form):
    description = forms.CharField(max_length=256)

class ProductIDForm(forms.Form):
    product_id = forms.IntegerField()

class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget = forms.PasswordInput(), max_length = 32)
    new_password = forms.CharField(widget = forms.PasswordInput(), max_length = 32)
    new_password_confirm = forms.CharField(widget = forms.PasswordInput(), max_length = 32)

class PayForm(forms.Form):
    order_id = forms.IntegerField()

class PayFinish(forms.Form):
    token = forms.CharField(max_length = 32)
    order_id = forms.IntegerField()

class PayCancel(forms.Form):
    token = forms.CharField(max_length = 32)
    order_id = forms.IntegerField()

class CommentForm(forms.Form):
    stars = forms.IntegerField(min_value=1, max_value=3)
    comment_text = forms.CharField(max_length=256)

class CheckForm(forms.Form):
    product_id = forms.IntegerField()
    state = forms.IntegerField(min_value=0, max_value=1)

class EmailBindForm(forms.Form):
    email = forms.EmailField()

class ConfirmForm(forms.Form):
    key = forms.CharField(max_length = 4)

class PayBindForm(forms.Form):
    payment = forms.CharField(max_length=32)
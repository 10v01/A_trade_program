from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label = '用户名', max_length = 16)
    password = forms.CharField(label = '密码', widget = forms.PasswordInput(), max_length = 32)

class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', max_length = 16)
    password = forms.CharField(label = '密码', widget = forms.PasswordInput(), max_length = 32)
    confirm_password = forms.CharField(label = '确认密码', widget = forms.PasswordInput(), max_length = 32)
    paypassword = forms.CharField(label = '支付密码', widget = forms.PasswordInput(), max_length = 32)
    paypassword_confirm = forms.CharField(label = '确认支付密码', widget = forms.PasswordInput(), max_length = 32)

class ConfirmForm(forms.Form):
    password = forms.CharField(label='密码', widget=forms.PasswordInput(), max_length=32)
    state = forms.IntegerField(min_value=0, max_value=1)
# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.template.loader import get_template
from django.http import HttpResponse
from login import models, forms
from django.middleware.csrf import get_token
from .forms import LoginForm

# Create your views here.

def index(request, pid = None, del_pass = None):
    if 'username' in request.session:
        username = request.session['username']
        useremail = request.session['useremail']
    template = get_template('index.html')
    html = template.render(locals())
    return HttpResponse(html)

def login(request):
    message = ""
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            login_name = request.POST['username'].strip()
            login_password = request.POST['password']
            try:
                user = models.User.objects.get(name = login_name)
                if user.password == login_password:
                    response = redirect('/')
                    request.session['username'] = user.name
                    request.session['useremail'] = user.email
                    return redirect('/')
                else:
                    message = "密码错误，请重试"
            except:
                message = "服务器异常"
        else:
            message = "请检查输入的字段内容"
    else:
        login_form = forms.LoginForm()

    return render(request, 'login.html', {'form': login_form, 'message': message})

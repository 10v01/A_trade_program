# -*- coding: UTF-8 -*-
from django.shortcuts import render
from mainsite import models, forms
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime

# Create your views here.

def index(request, pid = None, del_pass = None):
    if request.user.is_authenticated:
        username = request.user.username
    messages.get_messages(request)
    TheTimeOfNow = datetime.now()
    return render(request,'index.html',locals())

@login_required(login_url='/login/')
def userinfo(request):
    if request.user.is_authenticated:
        username = request.user.username
        try:
            userinfo = User.objects.get(username = username)
        except:
            pass
    TheTimeOfNow = datetime.now()
    return render(request, 'userinfo.html', locals())

def login(request):
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            login_name = request.POST['username'].strip()
            login_password = request.POST['password']
            user = authenticate(username = login_name, password = login_password)
            if user is not None:
                if user.is_active:
                    auth.login(request,user)
                    messages.add_message(request,messages.SUCCESS,"成功登录了")
                    return redirect('/')
                else:
                    messages.add_message(request,messages.WARNING,"账户未启用")
            else:
                messages.add_message(request, messages.WARNING,"登录失败")
        else:
            messages.add_message(request, messages.INFO, "请检查输入字段的内容")
    else:
        login_form = forms.LoginForm()
    TheTimeOfNow = datetime.now()
    return render(request,'login.html',locals())

def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.INFO, "成功注销了")
    return redirect('/')

def register(request):
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():
            register_name = request.POST['username'].strip()
            register_password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            if confirm_password == register_password:
                try:
                    user_exist = User.objects.get(username = register_name)
                    messages.add_message(request, messages.WARNING, "此用户名已被注册")
                except:
                    User.objects.create_user(register_name, '', register_password)
                    messages.add_message(request, messages.SUCCESS, "注册成功")
                    return redirect('/')
            else:
                messages.add_message(request, messages.WARNING, "两次输入的密码不符")
        else:
            messages.add_message(request, messages.INFO, "请检查输入字段的内容")
    else:
        login_form = forms.LoginForm()
    TheTimeOfNow = datetime.now()
    return render(request,'register.html',locals())

def mylist(request):
    TheTimeOfNow = datetime.now()
    return render(request, 'mylist.html', locals())

def mymark(request):
    TheTimeOfNow = datetime.now()
    return render(request, 'mymark.html', locals())

def mycart(request):
    TheTimeOfNow = datetime.now()
    return render(request, 'mycart.html', locals())

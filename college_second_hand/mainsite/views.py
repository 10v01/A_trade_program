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
from django.core import paginator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request, pid = None, del_pass = None):
    if request.user.is_authenticated:
        username = request.user.username
    messages.get_messages(request)
    all_products = models.Product.objects.filter(state = 0).order_by("-uid")
    paginator_cur = paginator.Paginator(all_products, 5)
    p = request.GET.get('p')
    try:
        products = paginator_cur.page(p)
    except paginator.PageNotAnInteger:
        products = paginator_cur.page(1)
    except paginator.EmptyPage:
        products = paginator_cur.page(paginator_cur.num_pages)
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
    if request.user.is_authenticated:
        username = request.user.username
        messages.add_message(request, messages.INFO, "您已登录")
        return redirect('/')
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
    if request.user.is_authenticated:
        auth.logout(request)
        messages.add_message(request, messages.INFO, "成功注销了")
        return redirect('/')
    else:
        messages.add_message(request, messages.WARNING, "尚未登录")
        return redirect('/')

def register(request):
    if request.user.is_authenticated:
        username = request.user.username
        messages.add_message(request, messages.INFO, "您已登录")
        return redirect('/')
    else:
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
                        current_user = User.objects.create_user(register_name, '', register_password)
                        models.Profile.objects.create(user = current_user)
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

def product(request, product_uid):
    if request.user.is_authenticated:
        username = request.user.username
    TheTimeOfNow = datetime.now()
    id = product_uid
    return render(request, 'product.html', locals())

@login_required(login_url='/login/')
def mylist(request):
    if request.user.is_authenticated:
        username = request.user.username
    TheTimeOfNow = datetime.now()
    return render(request, 'mylist.html', locals())

@login_required(login_url='/login/')
def mymark(request):
    if request.user.is_authenticated:
        username = request.user.username
    TheTimeOfNow = datetime.now()
    return render(request, 'mymark.html', locals())

@login_required(login_url='/login/')
def mycart(request):
    if request.user.is_authenticated:
        username = request.user.username
    TheTimeOfNow = datetime.now()
    return render(request, 'mycart.html', locals())

def pay(request, product_uid):
    if request.user.is_authenticated:
        username = request.user.username
        if request.method == 'POST':
            passwd = request.POST['password']
            user = authenticate(username=username, password=passwd)
            if user is not None:
                messages.add_message(request, messages.SUCCESS, "成功(WIP)")
                return render(request, 'pay.html', locals())
            else:
                messages.add_message(request, messages.WARNING, "密码错误")
                return render(request, 'pay.html', locals())
    else:
        messages.add_message(request, messages.WARNING, "尚未登录")
        return redirect('/login')

    TheTimeOfNow = datetime.now()
    return render(request, 'pay.html', locals())
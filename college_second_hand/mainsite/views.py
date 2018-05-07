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
    TheTimeOfNow = datetime.now()
    if request.user.is_authenticated:
        username = request.user.username
    messages.get_messages(request)
    all_products = models.Product.objects.filter(state = 0).order_by("-id")
    paginator_cur = paginator.Paginator(all_products, 5)
    p = request.GET.get('p')
    try:
        products = paginator_cur.page(p)
    except paginator.PageNotAnInteger:
        products = paginator_cur.page(1)
    except paginator.EmptyPage:
        products = paginator_cur.page(paginator_cur.num_pages)
    return render(request,'index.html',locals())

@login_required(login_url='/login/')
def userinfo(request):
    TheTimeOfNow = datetime.now()
    if request.user.is_authenticated:
        username = request.user.username
        userinfo = models.Profile.objects.get(user = request.user)
    return render(request, 'userinfo.html', locals())

def login(request):
    TheTimeOfNow = datetime.now()
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
    TheTimeOfNow = datetime.now()
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
                    user_exist = User.objects.filter(username = register_name).exists()
                    if user_exist:
                        messages.add_message(request, messages.WARNING, "此用户名已被注册")
                    else:
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
        return render(request,'register.html',locals())

def product(request, product_id):
    TheTimeOfNow = datetime.now()
    if request.user.is_authenticated:
        username = request.user.username
    product = models.Product.objects.get(id = product_id)
    return render(request, 'product.html', locals())

@login_required(login_url='/login/')
def mylist(request):
    TheTimeOfNow = datetime.now()
    if request.user.is_authenticated:
        username = request.user.username
    return render(request, 'mylist.html', locals())

@login_required(login_url='/login/')
def mymark(request):
    TheTimeOfNow = datetime.now()
    if request.user.is_authenticated:
        username = request.user.username
    return render(request, 'mymark.html', locals())

@login_required(login_url='/login/')
def mycart(request):
    TheTimeOfNow = datetime.now()
    if request.user.is_authenticated:
        username = request.user.username
    if request.user.is_authenticated:
        profile_cur = models.Profile.objects.get(user = request.user)
        all_orders = models.Order.objects.filter(buyer = profile_cur).order_by("-id")
        paginator_cur = paginator.Paginator(all_orders, 5)
        p = request.GET.get('p')
        try:
            orders = paginator_cur.page(p)
        except paginator.PageNotAnInteger:
            orders = paginator_cur.page(1)
        except paginator.EmptyPage:
            orders = paginator_cur.page(paginator_cur.num_pages)
    return render(request, 'mycart.html', locals())

@login_required(login_url='/login/')
def cart_add(request):
    TheTimeOfNow = datetime.now()
    if request.method != 'POST':
        return redirect('/')
    profile_cur = models.Profile.objects.get(user=request.user)
    if request.user.is_authenticated:
        username = request.user.username
    if request.user.is_authenticated:
        state = 0
        cart_add_form = forms.CartAddForm(request.POST)
        if cart_add_form.is_valid():
            product_id_cur = request.POST['product_id']
            try:
                product_cur = models.Product.objects.get(id = product_id_cur)
            except:
                messages.add_message(request, messages.WARNING, "此商品不存在")
                return redirect('/')
            if profile_cur.full_name == None:
                state = 1
                #messages.add_message(request, messages.WARNING, "请补充你的姓名")
            elif profile_cur.address == None:
                state = 2
                #messages.add_message(request, messages.WARNING, "请补充你的地址")
            elif profile_cur.phone == None:
                state = 3
                #messages.add_message(request, messages.WARNING, "请补充你的手机号")
            elif product_cur.seller == profile_cur:
                state = 4
                #messages.add_message(request, messages.WARNING, "啥？你想购买自己卖的物品？")
            elif product_cur.state != 0:
                state = 5
                #messages.add_message(request, messages.WARNING, "此商品不处于待售状态")
            elif models.Order.objects.filter(product = product_cur).exists():
                state = 6
                #messages.add_message(request, messages.WARNING, "此商品已在你的购物车中")
            else:
                state = 7
                models.Order.objects.create(buyer = profile_cur, product = product_cur, full_name = profile_cur.full_name, address = profile_cur.address, phone = profile_cur.phone)
        else:
            messages.add_message(request, messages.INFO, "请检查输入字段的内容")

    return render(request, 'cart_add.html', locals())

@login_required(login_url='/login/')
def cart_remove(request):
    TheTimeOfNow = datetime.now()
    if request.method != 'POST':
        return redirect('/mycart')
    if request.user.is_authenticated:
        profile_cur = models.Profile.objects.get(user=request.user)
        order_id_cur = request.POST['order_id']
        try:
            order_cur = models.Order.objects.get(id = order_id_cur)
        except:
            messages.add_message(request, messages.WARNING, "此订单不存在")
            return redirect('/')
    return redirect('/mycart')

@login_required(login_url='/login/')
def product_add(request):
    TheTimeOfNow = datetime.now()
    if request.user.is_authenticated:
        username = request.user.username
    if request.method == 'POST':
        product_add_form = forms.ProductForm(request.POST)
        if product_add_form.is_valid():
            profile_cur = models.Profile.objects.get(user = request.user)
            category_cur = models.Category.objects.get(id = request.POST['category'])
            price_cur = request.POST['price']
            name_cur = request.POST['name']
            description_cur = request.POST['description'].strip()
            if description_cur:
                models.Product.objects.create(seller = profile_cur, category = category_cur, price = price_cur,
                                              name = name_cur, description = description_cur, state = 0)
                messages.add_message(request, messages.INFO, "添加成功，已填写描述")
            else:
                models.Product.objects.create(seller = profile_cur, category = category_cur, price = price_cur,
                                              name = name_cur, state = 0)
                messages.add_message(request, messages.INFO, "添加成功，未填写描述")
        else:
            messages.add_message(request, messages.INFO, "请检查输入字段的内容")
    categories = models.Category.objects.all()
    return render(request,'product_add.html',locals())

@login_required(login_url='/login/')
def product_modify_select(request):
    TheTimeOfNow = datetime.now()
    if request.user.is_authenticated:
        username = request.user.username
    profile_cur = models.Profile.objects.get(user=request.user)
    all_products = models.Product.objects.filter(state=0, seller = profile_cur).order_by("-id")
    paginator_cur = paginator.Paginator(all_products, 5)
    p = request.GET.get('p')
    try:
        products = paginator_cur.page(p)
    except paginator.PageNotAnInteger:
        products = paginator_cur.page(1)
    except paginator.EmptyPage:
        products = paginator_cur.page(paginator_cur.num_pages)
    return render(request, 'product_modify_select.html', locals())

@login_required(login_url='/login/')
def product_modify(request, product_id):
    TheTimeOfNow = datetime.now()
    if request.user.is_authenticated:
        username = request.user.username
    profile_cur = models.Profile.objects.get(user=request.user)
    try:
        product_cur = models.Product.objects.get(id = product_id)
    except:
        messages.add_message(request, messages.WARNING, "这个商品不存在")
        return redirect('/product_modify/')
    if product_cur.seller != profile_cur:
        messages.add_message(request, messages.WARNING, "这个商品不属于你")
        return redirect('/product_modify/')
    if request.method == 'POST':
        product_modify_form = forms.ProductForm(request.POST)
        if product_modify_form.is_valid():
            product_cur.category = models.Category.objects.get(id=request.POST['category'])
            product_cur.price = request.POST['price']
            product_cur.name = request.POST['name']
            description_cur = request.POST['description'].strip()
            if description_cur:
                product_cur.description = description_cur
            else:
                product_cur.description = "暂无简介"
            product_cur.save()
            messages.add_message(request, messages.SUCCESS, "成功修改了商品信息")
        else:
            messages.add_message(request, messages.INFO, "请检查输入字段的内容")

    categories = models.Category.objects.all()
    return render(request,'product_modify.html',locals())

def pay(request, product_id):
    TheTimeOfNow = datetime.now()
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

    return render(request, 'pay.html', locals())
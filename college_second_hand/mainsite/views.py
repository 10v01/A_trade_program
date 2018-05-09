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
        profile_cur = models.Profile.objects.get(user=request.user)
    product = models.Product.objects.get(id = product_id)
    return render(request, 'product.html', locals())

@login_required(login_url='/login/')
def mymark(request):
    TheTimeOfNow = datetime.now()
    if request.user.is_authenticated:
        username = request.user.username
    if request.user.is_authenticated:
        profile_cur = models.Profile.objects.get(user=request.user)
        all_marks = models.Mark.objects.filter(marker=profile_cur).order_by("-id")
        paginator_cur = paginator.Paginator(all_marks, 5)
        p = request.GET.get('p')
        try:
            marks = paginator_cur.page(p)
        except paginator.PageNotAnInteger:
            marks = paginator_cur.page(1)
        except paginator.EmptyPage:
            marks = paginator_cur.page(paginator_cur.num_pages)
    return render(request, 'mymark.html', locals())

@login_required(login_url='/login/')
def myorder(request):
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
    return render(request, 'myorder.html', locals())

@login_required(login_url='/login/')
def mark_add(request):
    TheTimeOfNow = datetime.now()
    if request.method != 'POST':
        return redirect('/')
    profile_cur = models.Profile.objects.get(user=request.user)
    if request.user.is_authenticated:
        username = request.user.username
    if request.user.is_authenticated:
        state = 0
        mark_add_form = forms.MarkAddForm(request.POST)
        if mark_add_form.is_valid():
            product_id_cur = request.POST['product_id']
            try:
                product_cur = models.Product.objects.get(id=product_id_cur)
            except:
                messages.add_message(request, messages.WARNING, "此商品不存在")
                return redirect('/')
            if product_cur.seller == profile_cur:
                state = 1
            elif models.Mark.objects.filter(marker = profile_cur, product=product_cur).exists():
                state = 2
            else:
                state = 3
                models.Mark.objects.create(marker=profile_cur, product=product_cur)
        else:
            messages.add_message(request, messages.INFO, "请检查输入字段的内容")

    return render(request, 'mark_add.html', locals())

@login_required(login_url='/login/')
def mark_remove(request):
    if request.method != 'POST':
        return redirect('/mymark')
    if request.user.is_authenticated:
        profile_cur = models.Profile.objects.get(user=request.user)
        mark_remove_form = forms.MarkRemoveForm(request.POST)
        if not mark_remove_form.is_valid():
            messages.add_message(request, messages.INFO, "请检查输入字段的内容")
            return redirect('/mymark')
        mark_id_cur = request.POST['mark_id']
        try:
            mark_cur = models.Mark.objects.get(id=mark_id_cur)
        except:
            messages.add_message(request, messages.WARNING, "此收藏不存在")
            return redirect('/mymark')
        if mark_cur.marker == profile_cur:
            mark_cur.delete()
            messages.add_message(request, messages.SUCCESS, "删除成功")
        else:
            messages.add_message(request, messages.WARNING, "此收藏不属于你")
    return redirect('/mymark')

@login_required(login_url='/login/')
def order_add(request):
    TheTimeOfNow = datetime.now()
    if request.method != 'POST':
        return redirect('/')
    profile_cur = models.Profile.objects.get(user=request.user)
    if request.user.is_authenticated:
        username = request.user.username
    if request.user.is_authenticated:
        state = 0
        order_add_form = forms.OrderAddForm(request.POST)
        if order_add_form.is_valid():
            product_id_cur = request.POST['product_id']
            try:
                product_cur = models.Product.objects.get(id = product_id_cur)
            except:
                messages.add_message(request, messages.WARNING, "此商品不存在")
                return redirect('/')
            if profile_cur.full_name == None:
                state = 1
            elif profile_cur.address == None:
                state = 2
            elif profile_cur.phone == None:
                state = 3
            elif product_cur.seller == profile_cur:
                state = 4
            elif models.Order.objects.filter(buyer = profile_cur, product = product_cur).exists():
                state = 5
            elif product_cur.state != 0:
                state = 6
            else:
                state = 7
                models.Order.objects.create(buyer = profile_cur, product = product_cur, full_name = profile_cur.full_name,
                                            address = profile_cur.address, phone = profile_cur.phone, price = product_cur.price)
                product_cur.state = 1
                product_cur.save()
        else:
            messages.add_message(request, messages.INFO, "请检查输入字段的内容")

    return render(request, 'order_add.html', locals())

@login_required(login_url='/login/')
def order_remove(request):
    if request.method != 'POST':
        return redirect('/myorder')
    if request.user.is_authenticated:
        profile_cur = models.Profile.objects.get(user=request.user)
        order_remove_form = forms.OrderRemoveForm(request.POST)
        if not order_remove_form.is_valid():
            messages.add_message(request, messages.INFO, "请检查输入字段的内容")
            return redirect('/myorder')
        order_id_cur = request.POST['order_id']
        try:
            order_cur = models.Order.objects.get(id=order_id_cur)
        except:
            messages.add_message(request, messages.WARNING, "此订单不存在")
            return redirect('/myorder')
        if order_cur.buyer == profile_cur:
            order_cur.delete()
            order_cur.product.state = 0
            order_cur.product.save()
            messages.add_message(request, messages.SUCCESS, "删除成功")
        else:
            messages.add_message(request, messages.WARNING, "此订单不属于你")
    return redirect('/myorder')

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
def myproduct(request):
    TheTimeOfNow = datetime.now()
    if request.user.is_authenticated:
        username = request.user.username
    profile_cur = models.Profile.objects.get(user=request.user)
    all_products = models.Product.objects.filter(seller = profile_cur).order_by("-id")
    paginator_cur = paginator.Paginator(all_products, 5)
    p = request.GET.get('p')
    try:
        products = paginator_cur.page(p)
    except paginator.PageNotAnInteger:
        products = paginator_cur.page(1)
    except paginator.EmptyPage:
        products = paginator_cur.page(paginator_cur.num_pages)
    return render(request, 'myproduct.html', locals())

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
        return redirect('/myproduct/')
    if product_cur.seller != profile_cur:
        messages.add_message(request, messages.WARNING, "这个商品不属于你")
        return redirect('/myproduct/')
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

@login_required(login_url='/login/')
def product_remove(request):
    if request.method != 'POST':
        return redirect('/myproduct')
    if request.user.is_authenticated:
        profile_cur = models.Profile.objects.get(user=request.user)
        product_remove_form = forms.ProductRemoveForm(request.POST)
        if not product_remove_form.is_valid():
            messages.add_message(request, messages.INFO, "请检查输入字段的内容")
            return redirect('/myproduct')
        product_id_cur = request.POST['product_id']
        try:
            product_cur = models.Product.objects.get(id=product_id_cur)
        except:
            messages.add_message(request, messages.WARNING, "此商品不存在")
            return redirect('/myproduct')
        if product_cur.seller == profile_cur:
            product_cur.delete()
            messages.add_message(request, messages.SUCCESS, "删除成功")
        else:
            messages.add_message(request, messages.WARNING, "此商品不属于你")
    return redirect('/myproduct')

def search(request):
    TheTimeOfNow = datetime.now()
    if request.user.is_authenticated:
        username = request.user.username
    product_name = request.GET.get('product_name')
    all_products = models.Product.objects.filter(name__contains = product_name, state=0).order_by("-id")
    p = request.GET.get('p')
    paginator_cur = paginator.Paginator(all_products, 5)
    try:
        products = paginator_cur.page(p)
    except paginator.PageNotAnInteger:
        products = paginator_cur.page(1)
    except paginator.EmptyPage:
        products = paginator_cur.page(paginator_cur.num_pages)
    return render(request, 'search.html', locals())

@login_required(login_url='/login/')
def pay(request):
    TheTimeOfNow = datetime.now()
    if request.user.is_authenticated:
        username = request.user.username
    if request.method == 'POST':
        order_id_cur = request.POST['order_id']
        pay_form = forms.PayForm(request.POST)
        if not pay_form.is_valid():
            messages.add_message(request, messages.INFO, "请检查输入字段的内容")
            return redirect('/myorder')

    return render(request, 'pay.html', locals())

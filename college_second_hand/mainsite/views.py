# -*- coding: UTF-8 -*-
from django.shortcuts import render
import requests
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
import random

# Create your views here.

def index(request, pid = None, del_pass = None):
    TheTimeOfNow = datetime.now()
    if request.user.is_authenticated:
        username = request.user.username
        profile_cur = models.Profile.objects.get(user=request.user)
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
    messages.get_messages(request)
    if request.user.is_authenticated:
        username = request.user.username
        userinfo = models.Profile.objects.get(user = request.user)
        profile_cur = models.Profile.objects.get(user=request.user)
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
                        models.Profile.objects.create(user = current_user, id = current_user.id)
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
    if profile_cur.email is None:
        messages.add_message(request, messages.WARNING, "你还未通过邮箱身份验证")
        return redirect('/')
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
            if profile_cur.full_name is None:
                state = 1
            elif profile_cur.address is None:
                state = 2
            elif profile_cur.phone is None:
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
        order_remove_form = forms.OrderIDForm(request.POST)
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
            if order_cur.state == 1:
                messages.add_message(request, messages.WARNING, "请先到第三方平台取消支付状态")
                return redirect('/myorder')
            if order_cur.state == -1:
                messages.add_message(request, messages.WARNING, "此订单已被删除")
                return redirect('/myorder')
            if order_cur.state != 0:
                messages.add_message(request, messages.WARNING, "付款已完成，无法删除")
                return redirect('/myorder')
            if order_cur.product.state == 1:
                order_cur.product.state = 0
                order_cur.product.save()
            order_cur.state = -1
            order_cur.save()
            messages.add_message(request, messages.SUCCESS, "取消订单成功")
        else:
            messages.add_message(request, messages.WARNING, "此订单不属于你")
    return redirect('/myorder')

@login_required(login_url='/login/')
def product_add(request):
    TheTimeOfNow = datetime.now()
    if request.user.is_authenticated:
        username = request.user.username
    profile_cur = models.Profile.objects.get(user=request.user)
    if profile_cur.email is None:
        messages.add_message(request, messages.WARNING, "你还未通过邮箱身份验证")
        return redirect('/')
    if request.method == 'POST':
        product_add_form = forms.ProductForm(request.POST)
        if product_add_form.is_valid():
            category_cur = models.Category.objects.get(id = request.POST['category'])
            price_cur = request.POST['price']
            name_cur = request.POST['name']
            description_cur = request.POST['description'].strip()
            if description_cur:
                models.Product.objects.create(seller=profile_cur, category=category_cur, price=price_cur,
                                              name=name_cur, description=description_cur, state=-1)
                messages.add_message(request, messages.INFO, "添加成功，已填写描述")
            else:
                models.Product.objects.create(seller=profile_cur, category=category_cur, price=price_cur,
                                              name=name_cur, state=-1)
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
    if profile_cur.email is None:
        messages.add_message(request, messages.WARNING, "你还未通过邮箱身份验证")
        return redirect('/')
    try:
        product_cur = models.Product.objects.get(id = product_id)
    except:
        messages.add_message(request, messages.WARNING, "这个商品不存在")
        return redirect('/myproduct/')
    if product_cur.seller != profile_cur:
        messages.add_message(request, messages.WARNING, "这个商品不属于你")
        return redirect('/myproduct/')
    if product_cur.state != 0:
        messages.add_message(request, messages.WARNING, "此商品不处于待售状态")
        return redirect('/myproduct')
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
def profile_modify(request):
    TheTimeOfNow = datetime.now()
    if request.user.is_authenticated:
        username = request.user.username
    profile_cur = models.Profile.objects.get(user=request.user)
    if request.method == 'POST':
        profile_modify_form = forms.ProfileModifyForm(request.POST)
        if profile_modify_form.is_valid():
            profile_cur.sex = request.POST['sex']
            profile_cur.full_name = request.POST['full_name']
            profile_cur.phone = request.POST['phone']
            profile_cur.address = request.POST['address']
            profile_cur.save()
            profile_cur = models.Profile.objects.get(user=request.user)
            messages.add_message(request, messages.SUCCESS, "成功修改了用户信息")
        else:
            messages.add_message(request, messages.INFO, "请检查输入字段的内容")

    return render(request, 'profile_modify.html', locals())

@login_required(login_url='/login/')
def change_password(request):
    TheTimeOfNow = datetime.now()
    if request.user.is_authenticated:
        username = request.user.username
    profile_cur = models.Profile.objects.get(user=request.user)
    if request.method != 'POST':
        return render(request, 'change_password.html', locals())

    change_password_form = forms.ChangePasswordForm(request.POST)
    if not change_password_form.is_valid():
        messages.add_message(request, messages.INFO, "请检查输入字段的内容")
        return render(request, 'change_password.html', locals())

    new_password = request.POST['new_password']
    new_password_confirm = request.POST['new_password_confirm']
    if new_password != new_password_confirm:
        messages.add_message(request, messages.WARNING, "两次输入的密码不符")
        return render(request, 'change_password.html', locals())

    user_cur = authenticate(username = username, password = request.POST['password'])
    if user_cur is None:
        messages.add_message(request, messages.WARNING, "密码认证失败")
        return render(request, 'change_password.html', locals())

    user_cur.set_password(new_password)
    user_cur.save()
    messages.add_message(request, messages.SUCCESS, "密码修改成功")
    return render(request, 'change_password.html', locals())

@login_required(login_url='/login/')
def product_remove(request):
    if request.method != 'POST':
        return redirect('/myproduct')
    if request.user.is_authenticated:
        profile_cur = models.Profile.objects.get(user=request.user)
        product_remove_form = forms.ProductIDForm(request.POST)
        if not product_remove_form.is_valid():
            messages.add_message(request, messages.INFO, "请检查输入字段的内容")
            return redirect('/myproduct')
        product_id_cur = request.POST['product_id']
        try:
            product_cur = models.Product.objects.get(id=product_id_cur)
        except:
            messages.add_message(request, messages.WARNING, "此商品不存在")
            return redirect('/myproduct')
        if product_cur.state != 0:
            messages.add_message(request, messages.WARNING, "此商品不处于待售状态")
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
        profile_cur = models.Profile.objects.get(user=request.user)
    product_name = request.GET.get('product_name')
    try:
        all_products = models.Product.objects.filter(name__contains = product_name, state=0).order_by("-id")
    except:
        return redirect('/')
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
    profile_cur = models.Profile.objects.get(user=request.user)
    if request.method != 'POST':
        return redirect('/myorder')
    if profile_cur.email is None:
        messages.add_message(request, messages.WARNING, "你还未通过邮箱身份验证")
        return redirect('/')
    pay_form = forms.PayForm(request.POST)
    if not pay_form.is_valid():
        messages.add_message(request, messages.INFO, "请检查输入字段的内容")
        return redirect('/myorder')
    order_id = request.POST['order_id']
    try:
        order = models.Order.objects.get(id = order_id)
    except:
        messages.add_message(request, messages.WARNING, "订单编号错误")
        return redirect('/myorder')
    if order.buyer != profile_cur:
        messages.add_message(request, messages.WARNING, "此订单不属于你")
        return redirect('/myorder')
    if order.buyer.BoundPayment is None:
        messages.add_message(request, messages.WARNING, "你还未绑定支付账号")
        return redirect('/myorder')
    if order.product.seller.BoundPayment is None:
        messages.add_message(request, messages.WARNING, "卖家未绑定支付账号")
        return redirect('/myorder')

    url = 'http://127.0.0.1:10086/pay'
    d = {
        'payer': order.buyer.BoundPayment,
        'receiver': order.product.seller.BoundPayment,
        'amount': order.product.price,
        'order': order_id,
    }
    try:
        r = requests.post(url, data=d)
    except:
        messages.add_message(request, messages.WARNING, "系统繁忙")
        return redirect('/myorder')
    print(r.text)
    order.state = 1
    order.payment_id = r.text
    order.save()
    messages.add_message(request, messages.SUCCESS, "发送成功")
    return redirect('/myorder')

@csrf_exempt
def pay_finish(request):
    if request.method != "POST":
        return redirect('/')
    pay_finish_form = forms.PayFinish(request.POST)
    if not pay_finish_form.is_valid():
        return redirect('/')
    token = request.POST['token']
    order_id = request.POST['order_id']
    if token != "SKAMcjkso987UjPaqmcj012Kjidusjnb":
        return redirect('/')
    order_cur = models.Order.objects.get(id = order_id)
    order_cur.state = 2
    order_cur.save()
    order_cur.product.state = 2
    order_cur.product.save()
    return render(request, 'pay_finish.html', locals())

@csrf_exempt
def pay_cancel(request):
    if request.method != "POST":
        return redirect('/')
    pay_cancel_form = forms.PayCancel(request.POST)
    if not pay_cancel_form.is_valid():
        return redirect('/')
    token = request.POST['token']
    order_id = request.POST['order_id']
    if token != "SKAMcjkso987UjPaqmcj012Kjidusjnb":
        return redirect('/')
    order_cur = models.Order.objects.get(id = order_id)
    order_cur.state = 0
    order_cur.save()
    return render(request, 'pay_finish.html', locals())

@login_required(login_url='/login/')
def product_send(request):
    if request.method != "POST":
        return redirect('/myproduct')
    product_id_form = forms.ProductIDForm(request.POST)
    if not product_id_form.is_valid():
        messages.add_message(request, messages.INFO, "请检查输入字段的内容")
        return redirect('/myproduct')
    product_id = request.POST['product_id']
    try:
        product = models.Product.objects.get(id=product_id)
    except:
        messages.add_message(request, messages.WARNING, "商品编号处理异常")
        return redirect('/myproduct')
    if product.seller.user != request.user:
        messages.add_message(request, messages.WARNING, "商品不属于你")
        return redirect('/myproduct')
    if product.state != 2:
        messages.add_message(request, messages.WARNING, "商品不处于待发货状态")
        return redirect('/myproduct')
    try:
        order = models.Order.objects.get(product=product)
    except:
        messages.add_message(request, messages.WARNING, "买家订单异常")
        return redirect('/myproduct')
    product.state = 3
    product.save()
    order.state = 3
    order.save()
    messages.add_message(request, messages.SUCCESS, "成功")
    return redirect('/myproduct')

@login_required(login_url='/login/')
def order_receive(request):
    if request.method != "POST":
        return redirect('/myorder')
    order_id_form = forms.OrderIDForm(request.POST)
    if not order_id_form.is_valid():
        messages.add_message(request, messages.INFO, "请检查输入字段的内容")
        return redirect('/myorder')
    order_id = request.POST['order_id']
    try:
        order = models.Order.objects.get(id=order_id)
    except:
        messages.add_message(request, messages.WARNING, "订单编号处理异常")
        return redirect('/myorder')
    if order.buyer.user != request.user:
        messages.add_message(request, messages.WARNING, "订单不属于你")
        return redirect('/myorder')
    if order.state != 3:
        messages.add_message(request, messages.WARNING, "商品不处于待收货状态")
        return redirect('/myorder')
    product = order.product
    product.state = 4
    product.save()
    order.state = 4
    order.save()
    messages.add_message(request, messages.SUCCESS, "成功")
    return redirect('/myorder')

@login_required(login_url='/login/')
def comment(request, order_id):
    TheTimeOfNow = datetime.now()
    if request.user.is_authenticated:
        username = request.user.username
    profile_cur = models.Profile.objects.get(user=request.user)
    if request.method != 'POST':
        return render(request, 'comment.html', locals())
    comment_form = forms.CommentForm(request.POST)
    if not comment_form.is_valid():
        messages.add_message(request, messages.INFO, "请检查输入字段的内容")
        return render(request, 'comment.html', locals())
    try:
        order = models.Order.objects.get(id = order_id)
    except:
        messages.add_message(request, messages.WARNING, "订单编号处理异常")
        return render(request, 'comment.html', locals())
    if order.buyer != profile_cur:
        messages.add_message(request, messages.WARNING, "订单不属于你")
        return render(request, 'comment.html', locals())
    if order.state != 4:
        messages.add_message(request, messages.WARNING, "订单不处于待评价状态")
        return render(request, 'comment.html', locals())
    models.Comment.objects.create(order=order, stars=request.POST['stars'], comment_text=request.POST['comment_text'])
    order.state = 5
    order.save()
    order.product.state = 5
    order.product.save()
    messages.add_message(request, messages.SUCCESS, "评价成功")
    return redirect('/myorder')

@login_required(login_url='/login/')
def check(request):
    TheTimeOfNow = datetime.now()
    if not request.user.is_authenticated:
        return redirect('/login')
    username = request.user.username
    profile_cur = models.Profile.objects.get(user=request.user)
    if profile_cur.usertype != 1:
        messages.add_message(request, messages.WARNING, "你不是管理员")
        return redirect('/')
    if request.method == 'POST':
        check_form=forms.CheckForm(request.POST)
        if not check_form.is_valid():
            messages.add_message(request, messages.INFO, "请检查输入字段的内容")
            return redirect('/check')
        try:
            product = models.Product.objects.get(id = request.POST['product_id'])
        except:
            messages.add_message(request, messages.WARNING, "商品编号处理异常")
            return redirect('/check')
        if product.state != -2 and product.state != -1 and product.state != 0:
            messages.add_message(request, messages.WARNING, "此商品已被购买")
            return redirect('/check')
        state_cur = request.POST['state']
        if state_cur == '0':
            product.state = 0
            product.save()
            messages.add_message(request, messages.SUCCESS, "通过")
        if state_cur == '1':
            product.state = -2
            product.save()
            messages.add_message(request, messages.SUCCESS, "不通过")

    all_products = models.Product.objects.filter(state=-1).order_by("-id")
    paginator_cur = paginator.Paginator(all_products, 5)
    p = request.GET.get('p')
    try:
        products = paginator_cur.page(p)
    except paginator.PageNotAnInteger:
        products = paginator_cur.page(1)
    except paginator.EmptyPage:
        products = paginator_cur.page(paginator_cur.num_pages)
    return render(request, 'check.html', locals())

@login_required(login_url='/login/')
def checkall(request):
    TheTimeOfNow = datetime.now()
    if not request.user.is_authenticated:
        return redirect('/login')
    username = request.user.username
    profile_cur = models.Profile.objects.get(user=request.user)
    if profile_cur.usertype != 1:
        messages.add_message(request, messages.WARNING, "你不是管理员")
        return redirect('/')
    if request.method == 'POST':
        check_form=forms.CheckForm(request.POST)
        if not check_form.is_valid():
            messages.add_message(request, messages.INFO, "请检查输入字段的内容")
            return redirect('/checkall')
        try:
            product = models.Product.objects.get(id = request.POST['product_id'])
        except:
            messages.add_message(request, messages.WARNING, "商品编号处理异常")
            return redirect('/checkall')
        if product.state != -2 and product.state != -1 and product.state != 0:
            messages.add_message(request, messages.WARNING, "此商品已被购买")
            return redirect('/checkall')
        state_cur = request.POST['state']
        if state_cur == '0':
            product.state = 0
            product.save()
            messages.add_message(request, messages.SUCCESS, "通过")
        if state_cur == '1':
            product.state = -2
            product.save()
            messages.add_message(request, messages.SUCCESS, "不通过")

    all_products = models.Product.objects.all().order_by("-id")
    paginator_cur = paginator.Paginator(all_products, 5)
    p = request.GET.get('p')
    try:
        products = paginator_cur.page(p)
    except paginator.PageNotAnInteger:
        products = paginator_cur.page(1)
    except paginator.EmptyPage:
        products = paginator_cur.page(paginator_cur.num_pages)
    return render(request, 'checkall.html', locals())

@login_required(login_url='/login/')
def college_authenticate(request):
    TheTimeOfNow = datetime.now()
    if request.user.is_authenticated:
        username = request.user.username
    profile_cur = models.Profile.objects.get(user=request.user)
    if request.method != 'POST':
        return render(request, 'college_authenticate.html', locals())
    email_form = forms.EmailBindForm(request.POST)
    if not email_form.is_valid():
        messages.add_message(request, messages.INFO, "请检查输入字段的内容")
        return render(request, 'college_authenticate.html', locals())
    email = request.POST['email']
    profile_cur.email_binding = email
    key_gen = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = ""
    for i in range(4):
        k = random.randint(0, 61)
        key = key + key_gen[k]
    profile_cur.email_binding_key = key
    profile_cur.save()

    url = 'http://127.0.0.1:10086/email_binding'
    d = {
        'email': email,
        'key': key,
    }
    try:
        r = requests.post(url, data=d)
    except:
        messages.add_message(request, messages.WARNING, "系统繁忙")
        return render(request, 'bind_payment.html', locals())

    messages.add_message(request, messages.SUCCESS, "发送到邮箱成功")
    return redirect('/userinfo')

@login_required(login_url='/login/')
def college_authenticate_confirm(request):
    TheTimeOfNow = datetime.now()
    if request.user.is_authenticated:
        username = request.user.username
    profile_cur = models.Profile.objects.get(user=request.user)
    if request.method != 'POST':
        return render(request, 'college_authenticate_confirm.html', locals())
    confirm_form = forms.ConfirmForm(request.POST)
    if not confirm_form.is_valid():
        messages.add_message(request, messages.INFO, "请检查输入字段的内容")
        return render(request, 'college_authenticate_confirm.html', locals())
    key = request.POST['key']
    if key != profile_cur.email_binding_key:
        messages.add_message(request, messages.WARNING, "验证码错误")
        return render(request, 'college_authenticate_confirm.html', locals())
    profile_cur.email = profile_cur.email_binding
    profile_cur.email_binding = None
    profile_cur.email_binding_key = None
    profile_cur.save()
    messages.add_message(request, messages.SUCCESS, "绑定成功")
    return redirect('/userinfo')

@login_required(login_url='/login/')
def bind_payment(request):
    TheTimeOfNow = datetime.now()
    if request.user.is_authenticated:
        username = request.user.username
    profile_cur = models.Profile.objects.get(user=request.user)
    if request.method != 'POST':
        return render(request, 'bind_payment.html', locals())
    payment_form = forms.PayBindForm(request.POST)
    if not payment_form.is_valid():
        messages.add_message(request, messages.INFO, "请检查输入字段的内容")
        return render(request, 'bind_payment.html', locals())
    payment = request.POST['payment']
    profile_cur.pay_binding = payment
    key_gen = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = ""
    for i in range(4):
        k = random.randint(0, 61)
        key = key + key_gen[k]
    profile_cur.pay_binding_key = key
    profile_cur.save()

    url = 'http://127.0.0.1:10086/pay_binding'
    d = {
        'payment': payment,
        'key': key,
        'profile': profile_cur.user.username,
    }
    try:
        r = requests.post(url, data=d)
    except:
        messages.add_message(request, messages.WARNING, "系统繁忙")
        return render(request, 'bind_payment.html', locals())

    messages.add_message(request, messages.SUCCESS, "发送到第三方支付平台成功")
    return redirect('/userinfo')

@login_required(login_url='/login/')
def bind_payment_confirm(request):
    TheTimeOfNow = datetime.now()
    if request.user.is_authenticated:
        username = request.user.username
    profile_cur = models.Profile.objects.get(user=request.user)
    if request.method != 'POST':
        return render(request, 'bind_payment_confirm.html', locals())
    confirm_form = forms.ConfirmForm(request.POST)
    if not confirm_form.is_valid():
        messages.add_message(request, messages.INFO, "请检查输入字段的内容")
        return render(request, 'bind_payment_confirm.html', locals())
    key = request.POST['key']
    if key != profile_cur.pay_binding_key:
        messages.add_message(request, messages.WARNING, "验证码错误")
        return render(request, 'bind_payment_confirm.html', locals())
    profile_cur.BoundPayment = profile_cur.pay_binding
    profile_cur.pay_binding = None
    profile_cur.pay_binding_key = None
    profile_cur.save()
    messages.add_message(request, messages.SUCCESS, "绑定成功")
    return redirect('/userinfo')
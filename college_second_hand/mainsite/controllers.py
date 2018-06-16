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
from mainsite import External

class Account_control:
    def __init__(self, request):
        self.request = request
        self.TheTimeOfNow = datetime.now()

    def login(self):
        TheTimeOfNow = self.TheTimeOfNow
        if self.request.user.is_authenticated:
            messages.add_message(self.request, messages.INFO, "您已登录")
            return redirect('/')
        if self.request.method != 'POST':
            return render(self.request, 'login.html', locals())
        login_form = forms.LoginForm(self.request.POST)
        if not login_form.is_valid():
            messages.add_message(self.request, messages.INFO, "请检查输入字段的内容")
            return redirect('/login')
        login_name = self.request.POST['username'].strip()
        login_password = self.request.POST['password']
        user = authenticate(username=login_name, password=login_password)
        if user is None:
            messages.add_message(self.request, messages.WARNING, "登录失败")
            return redirect('/login')
        if not user.is_active:
            messages.add_message(self.request, messages.WARNING, "账户未启用")
            return redirect('/login')
        auth.login(self.request, user)
        messages.add_message(self.request, messages.SUCCESS, "登录成功")
        return redirect('/')

    def logout(self):
        if self.request.user.is_authenticated:
            auth.logout(self.request)
            messages.add_message(self.request, messages.SUCCESS, "成功注销")
            return redirect('/')
        else:
            messages.add_message(self.request, messages.WARNING, "尚未登录")
            return redirect('/')

    def register(self):
        TheTimeOfNow = self.TheTimeOfNow
        if self.request.user.is_authenticated:
            messages.add_message(self.request, messages.INFO, "您已登录")
            return redirect('/')
        if self.request.method != 'POST':
            return render(self.request, 'register.html', locals())
        register_form = forms.RegisterForm(self.request.POST)
        if not register_form.is_valid():
            messages.add_message(self.request, messages.INFO, "请检查输入字段的内容")
            return render(self.request, 'register.html', locals())
        register_name = self.request.POST['username'].strip()
        register_password = self.request.POST['password']
        confirm_password = self.request.POST['confirm_password']
        if confirm_password != register_password:
            messages.add_message(self.request, messages.WARNING, "两次输入的密码不符")
            return render(self.request, 'register.html', locals())
        user_exist = User.objects.filter(username=register_name).exists()
        if user_exist:
            messages.add_message(self.request, messages.WARNING, "此用户名已被注册")
            return render(self.request, 'register.html', locals())
        current_user = User.objects.create_user(register_name, '', register_password)
        models.Profile.objects.create(user=current_user, id=current_user.id)
        messages.add_message(self.request, messages.SUCCESS, "注册成功")
        return redirect('/')

    def modify(self):
        TheTimeOfNow = datetime.now()
        if not self.request.user.is_authenticated:
            messages.add_message(self.request, messages.WARNING, "请登录")
            return redirect('/')
        username = self.request.user.username
        profile_cur = models.Profile.objects.get(user=self.request.user)
        if self.request.method == 'POST':
            profile_modify_form = forms.ProfileModifyForm(self.request.POST)
            if profile_modify_form.is_valid():
                profile_cur.sex = self.request.POST['sex']
                profile_cur.full_name = self.request.POST['full_name']
                profile_cur.phone = self.request.POST['phone']
                profile_cur.address = self.request.POST['address']
                profile_cur.save()
                profile_cur = models.Profile.objects.get(user=self.request.user)
                messages.add_message(self.request, messages.SUCCESS, "成功修改了用户信息")
            else:
                messages.add_message(self.request, messages.INFO, "请检查输入字段的内容")
        return render(self.request, 'profile_modify.html', locals())

    def change_password(self):
        if not self.request.user.is_authenticated:
            messages.add_message(self.request, messages.WARNING, "请登录")
            return redirect('/')
        TheTimeOfNow = datetime.now()
        username = self.request.user.username
        profile_cur = models.Profile.objects.get(user=self.request.user)
        if self.request.method != 'POST':
            return render(self.request, 'change_password.html', locals())

        change_password_form = forms.ChangePasswordForm(self.request.POST)
        if not change_password_form.is_valid():
            messages.add_message(self.request, messages.INFO, "请检查输入字段的内容")
            return render(self.request, 'change_password.html', locals())

        new_password = self.request.POST['new_password']
        new_password_confirm = self.request.POST['new_password_confirm']
        if new_password != new_password_confirm:
            messages.add_message(self.request, messages.WARNING, "两次输入的密码不符")
            return render(self.request, 'change_password.html', locals())

        user_cur = authenticate(username=username, password=self.request.POST['password'])
        if user_cur is None:
            messages.add_message(self.request, messages.WARNING, "密码认证失败")
            return render(self.request, 'change_password.html', locals())

        user_cur.set_password(new_password)
        user_cur.save()
        messages.add_message(self.request, messages.SUCCESS, "密码修改成功")
        return render(self.request, 'change_password.html', locals())

class User_authenticate:
    def __init__(self, request):
        self.request = request
        self.user = request.user
        if request.user.is_authenticated:
            self.profile = models.Profile.objects.get(user=request.user)

    def is_admin(self):
        if not self.request.user.is_authenticated:
            return False
        return self.profile.usertype == 1

    def is_college_authenticated(self):
        if not self.request.user.is_authenticated:
            return False
        return self.profile.email is not None

    def has_bound_payment(self):
        if not self.request.user.is_authenticated:
            return False
        return self.profile.BoundPayment is not None

    def can_add_product(self):
        return self.is_college_authenticated() and self.has_bound_payment()

    def cannot_buy(self):
        if not self.is_college_authenticated():
            return 1
        elif not self.has_bound_payment():
            return 2
        elif self.profile.full_name is None:
            return 3
        elif self.profile.address is None:
            return 4
        elif self.profile.phone is None:
            return 5
        else:
            return 0

class Product_control:
    def __init__(self, request):
        self.request = request
        self.user = request.user
        if request.user.is_authenticated:
            self.profile = models.Profile.objects.get(user=request.user)

    def add(self):
        if not self.request.user.is_authenticated:
            messages.add_message(self.request, messages.WARNING, "请登录")
            return redirect('/')
        TheTimeOfNow = datetime.now()
        username = self.user.username
        profile_cur = self.profile
        categories = models.Category.objects.all()
        if self.request.method != 'POST':
            return render(self.request, 'product_add.html', locals())
        product_add_form = forms.ProductForm(self.request.POST)
        if not product_add_form.is_valid():
            messages.add_message(self.request, messages.INFO, "请检查输入字段的内容")
            return redirect('/')
        cur_auth = User_authenticate(self.request)
        can_add_product = cur_auth.can_add_product()
        if not can_add_product:
            messages.add_message(self.request, messages.WARNING, "你还未通过邮箱身份验证或还未绑定支付账号")
            return redirect('/')
        category_cur = models.Category.objects.get(id=self.request.POST['category'])
        price_cur = self.request.POST['price']
        name_cur = self.request.POST['name']
        description_cur = self.request.POST['description'].strip()
        if description_cur:
            models.Product.objects.create(seller=self.profile, category=category_cur, price=price_cur,
                                          name=name_cur, description=description_cur, state=-1)
        else:
            models.Product.objects.create(seller=self.profile, category=category_cur, price=price_cur,
                                          name=name_cur, state=-1)
        messages.add_message(self.request, messages.SUCCESS, "添加成功")
        return redirect('/')

    def modify(self, product_id):
        if not self.request.user.is_authenticated:
            messages.add_message(self.request, messages.WARNING, "请登录")
            return redirect('/')
        try:
            self.product = models.Product.objects.get(id=product_id)
        except:
            messages.add_message(self.request, messages.WARNING, "商品不存在")
            return redirect('/')
        cur_auth = User_authenticate(self.request)
        can_add_product = cur_auth.can_add_product()
        if not can_add_product:
            messages.add_message(self.request, messages.WARNING, "你还未通过邮箱身份验证或还未绑定支付账号")
            return redirect('/')
        if self.product.seller != self.profile:
            messages.add_message(self.request, messages.WARNING, "商品不属于你")
            return redirect('/')
        if self.product.state > 0:
            messages.add_message(self.request, messages.WARNING, "商品已被购买")
            return redirect('/')
        if self.request.method != 'POST':
            TheTimeOfNow = datetime.now()
            username = self.user.username
            profile_cur = self.profile
            categories = models.Category.objects.all()
            product_cur = self.product
            return render(self.request, 'product_modify.html', locals())
        product_modify_form = forms.ProductForm(self.request.POST)
        if not product_modify_form.is_valid():
            messages.add_message(self.request, messages.INFO, "请检查输入字段的内容")
            return redirect('/')
        self.product.category = models.Category.objects.get(id=self.request.POST['category'])
        self.product.price = self.request.POST['price']
        self.product.name = self.request.POST['name']
        description_cur = self.request.POST['description'].strip()
        if description_cur:
            self.product.description = description_cur
        else:
            self.product.description = "暂无简介"
        self.product.save()
        messages.add_message(self.request, messages.SUCCESS, "修改成功")
        return redirect('/')

    def remove(self):
        if not self.request.user.is_authenticated:
            messages.add_message(self.request, messages.WARNING, "请登录")
            return redirect('/')
        if self.request.method != 'POST':
            return redirect('/myproduct')
        product_remove_form = forms.ProductIDForm(self.request.POST)
        if not product_remove_form.is_valid():
            messages.add_message(self.request, messages.INFO, "请检查输入字段的内容")
            return redirect('/myproduct')
        try:
            self.product = models.Product.objects.get(id=self.request.POST['product_id'])
        except:
            messages.add_message(self.request, messages.WARNING, "商品不存在")
            return redirect('/myproduct')
        if self.product.seller != self.profile:
            messages.add_message(self.request, messages.WARNING, "商品不属于你")
            return redirect('/myproduct')
        if self.product.state > 0:
            messages.add_message(self.request, messages.WARNING, "商品已被购买或提交订单")
            return redirect('/myproduct')
        self.product.delete()
        messages.add_message(self.request, messages.SUCCESS, "删除成功")
        return redirect('/myproduct')

class Order_control:
    def __init__(self, request):
        self.request = request
        self.user = request.user
        if request.user.is_authenticated:
            self.profile = models.Profile.objects.get(user=request.user)
        self.TheTimeOfNow = datetime.now()

    def add(self):
        TheTimeOfNow = self.TheTimeOfNow
        username = self.user
        if self.request.method != 'POST':
            return redirect('/')
        if not self.request.user.is_authenticated:
            messages.add_message(self.request, messages.WARNING, "请登录")
            return redirect('/')
        profile_cur = self.profile
        order_add_form = forms.OrderAddForm(self.request.POST)
        if not order_add_form.is_valid():
            messages.add_message(self.request, messages.INFO, "请检查输入字段的内容")
            return redirect('/')
        try:
            self.product = models.Product.objects.get(id=self.request.POST['product_id'])
        except:
            messages.add_message(self.request, messages.WARNING, "商品不存在")
            return redirect('/')
        cur_auth = User_authenticate(self.request)
        cannot_buy = cur_auth.cannot_buy()
        if cannot_buy:
            result = cannot_buy
            return render(self.request, 'order_add.html', locals())
        if self.product.seller == self.profile:
            result = 6
            return render(self.request, 'order_add.html', locals())
        if self.product.state != 0:
            result = 7
            return render(self.request, 'order_add.html', locals())
        models.Order.objects.create(buyer=self.profile, product=self.product, full_name=self.profile.full_name,
                                    address=self.profile.address, phone=self.profile.phone, price=self.product.price)
        self.product.state = 1
        self.product.save()
        result = 0
        return render(self.request, 'order_add.html', locals())

    def remove(self):
        if self.request.method != 'POST':
            return redirect('/myorder')
        if not self.request.user.is_authenticated:
            messages.add_message(self.request, messages.WARNING, "请登录")
            return redirect('/')
        order_remove_form = forms.OrderIDForm(self.request.POST)
        if not order_remove_form.is_valid():
            messages.add_message(self.request, messages.INFO, "请检查输入字段的内容")
            return redirect('/myorder')
        try:
            self.order = models.Order.objects.get(id=self.request.POST['order_id'])
        except:
            messages.add_message(self.request, messages.WARNING, "订单不存在")
            return redirect('/myorder')
        if self.order.buyer != self.profile:
            messages.add_message(self.request, messages.WARNING, "订单不属于你")
            return redirect('/myorder')
        if self.order.state == 1:
            messages.add_message(self.request, messages.WARNING, "请先去第三方平台取消支付")
            return redirect('/myorder')
        if self.order.state != 0:
            messages.add_message(self.request, messages.WARNING, "订单已付款，无法删除")
            return redirect('/myorder')
        if self.order.product.state == 1:
            self.order.product.state = 0
            self.order.product.save()
        self.order.delete()
        messages.add_message(self.request, messages.SUCCESS, "删除成功")
        return redirect('/myorder')

class Payment_control:
    def __init__(self, request):
        self.request = request
        self.user = request.user
        if request.user.is_authenticated:
            self.profile = models.Profile.objects.get(user=request.user)
        self.TheTimeOfNow = datetime.now()

    # 这个方法依赖了Ibilling类。
    # C++中等价写法为HttpResponse pay(IBilling Billing_cur)
    # 但是python函数参数不需要指明数据类型
    # 事实上，在代码层面上，即使将IBilling类的代码全部删除，只留下Billing类，也不会出现报错。
    # 为了与建模一致，以及代码规范，保留了接口类。
    def pay(self, billing_cur):
        profile_cur = models.Profile.objects.get(user=self.request.user)
        if self.request.method != 'POST':
            return redirect('/myorder')
        if profile_cur.email is None:
            messages.add_message(self.request, messages.WARNING, "你还未通过邮箱身份验证")
            return redirect('/')
        pay_form = forms.PayForm(self.request.POST)
        if not pay_form.is_valid():
            messages.add_message(self.request, messages.INFO, "请检查输入字段的内容")
            return redirect('/myorder')
        order_id = self.request.POST['order_id']
        method = "testpay"
        try:
            self.order = models.Order.objects.get(id=order_id)
        except:
            messages.add_message(self.request, messages.WARNING, "订单编号错误")
            return redirect('/myorder')
        if self.order.buyer != profile_cur:
            messages.add_message(self.request, messages.WARNING, "此订单不属于你")
            return redirect('/myorder')
        if self.order.state != 0:
            messages.add_message(self.request, messages.WARNING, "订单不处于待提交状态")
            return redirect('/myorder')
        if self.order.buyer.BoundPayment is None:
            messages.add_message(self.request, messages.WARNING, "你还未绑定支付账号")
            return redirect('/myorder')
        if self.order.product.seller.BoundPayment is None:
            messages.add_message(self.request, messages.WARNING, "卖家未绑定支付账号")
            return redirect('/myorder')

        r = billing_cur.send_payment_info(self.order, method)

        if r is None:
            messages.add_message(self.request, messages.WARNING, "系统繁忙")
            return redirect('/myorder')
        self.order.state = 1
        self.order.payment_id = r.text
        self.order.save()
        messages.add_message(self.request, messages.SUCCESS, "发送成功")
        return redirect('/myorder')

class Pay_result_control:
    def pay_finish(self, order):
        order.state = 2
        order.save()
        order.product.state = 2
        order.product.save()
        return

    def pay_cancel(self, order):
        order.state = 0
        order.save()
        return

class College_authenticate_control:
    def __init__(self, request):
        self.request = request
        self.user = request.user
        if request.user.is_authenticated:
            self.profile = models.Profile.objects.get(user=request.user)

    def authenticate(self, email_sending_cur):
        TheTimeOfNow = datetime.now()
        if self.request.user.is_authenticated:
            username = self.request.user.username
        profile_cur = models.Profile.objects.get(user=self.request.user)
        if self.request.method != 'POST':
            return render(self.request, 'college_authenticate.html', locals())
        email_form = forms.EmailBindForm(self.request.POST)
        if not email_form.is_valid():
            messages.add_message(self.request, messages.INFO, "请检查输入字段的内容")
            return render(self.request, 'college_authenticate.html', locals())
        email = self.request.POST['email']
        profile_cur.email_binding = email
        key_gen = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        key = ""
        for i in range(4):
            k = random.randint(0, 61)
            key = key + key_gen[k]
        profile_cur.email_binding_key = key
        profile_cur.save()

        r = email_sending_cur.send_email(email, key)

        if r is None:
            messages.add_message(self.request, messages.WARNING, "系统繁忙")
            return redirect('/college_authenticate')

        messages.add_message(self.request, messages.SUCCESS, "发送到邮箱成功")
        return redirect('/userinfo')

    def authenticate_confirm(self):
        TheTimeOfNow = datetime.now()
        if self.request.user.is_authenticated:
            username = self.request.user.username
        profile_cur = models.Profile.objects.get(user=self.request.user)
        if self.request.method != 'POST':
            return render(self.request, 'college_authenticate_confirm.html', locals())
        confirm_form = forms.ConfirmForm(self.request.POST)
        if not confirm_form.is_valid():
            messages.add_message(self.request, messages.INFO, "请检查输入字段的内容")
            return render(self.request, 'college_authenticate_confirm.html', locals())
        key = self.request.POST['key']
        if key != profile_cur.email_binding_key:
            messages.add_message(self.request, messages.WARNING, "验证码错误")
            return render(self.request, 'college_authenticate_confirm.html', locals())
        profile_cur.email = profile_cur.email_binding
        profile_cur.email_binding = None
        profile_cur.email_binding_key = None
        profile_cur.save()
        messages.add_message(self.request, messages.SUCCESS, "绑定成功")
        return redirect('/userinfo')

class Bind_payment_control:
    def __init__(self, request):
        self.request = request
        self.user = request.user
        if request.user.is_authenticated:
            self.profile = models.Profile.objects.get(user=request.user)

    def bind(self):
        TheTimeOfNow = datetime.now()
        if self.request.user.is_authenticated:
            username = self.request.user.username
        profile_cur = models.Profile.objects.get(user=self.request.user)
        if self.request.method != 'POST':
            return render(self.request, 'bind_payment.html', locals())
        payment_form = forms.PayBindForm(self.request.POST)
        if not payment_form.is_valid():
            messages.add_message(self.request, messages.INFO, "请检查输入字段的内容")
            return render(self.request, 'bind_payment.html', locals())
        payment = self.request.POST['payment']
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
            messages.add_message(self.request, messages.WARNING, "系统繁忙")
            return render(self.request, 'bind_payment.html', locals())

        messages.add_message(self.request, messages.SUCCESS, "发送到第三方支付平台成功")
        return redirect('/userinfo')

    def bind_confirm(self):
        TheTimeOfNow = datetime.now()
        if self.request.user.is_authenticated:
            username = self.request.user.username
        profile_cur = models.Profile.objects.get(user=self.request.user)
        if self.request.method != 'POST':
            return render(self.request, 'bind_payment_confirm.html', locals())
        confirm_form = forms.ConfirmForm(self.request.POST)
        if not confirm_form.is_valid():
            messages.add_message(self.request, messages.INFO, "请检查输入字段的内容")
            return render(self.request, 'bind_payment_confirm.html', locals())
        key = self.request.POST['key']
        if key != profile_cur.pay_binding_key:
            messages.add_message(self.request, messages.WARNING, "验证码错误")
            return render(self.request, 'bind_payment_confirm.html', locals())
        profile_cur.BoundPayment = profile_cur.pay_binding
        profile_cur.pay_binding = None
        profile_cur.pay_binding_key = None
        profile_cur.save()
        messages.add_message(self.request, messages.SUCCESS, "绑定成功")
        return redirect('/userinfo')

class Comment_control:
    def __init__(self, request):
        self.request = request
        self.user = request.user
        if request.user.is_authenticated:
            self.profile = models.Profile.objects.get(user=request.user)

    def comment(self, order_id):
        TheTimeOfNow = datetime.now()
        if self.request.user.is_authenticated:
            username = self.request.user.username
        profile_cur = models.Profile.objects.get(user=self.request.user)
        if self.request.method != 'POST':
            return render(self.request, 'comment.html', locals())
        comment_form = forms.CommentForm(self.request.POST)
        if not comment_form.is_valid():
            messages.add_message(self.request, messages.INFO, "请检查输入字段的内容")
            return render(self.request, 'comment.html', locals())
        try:
            order = models.Order.objects.get(id=order_id)
        except:
            messages.add_message(self.request, messages.WARNING, "订单编号处理异常")
            return render(self.request, 'comment.html', locals())
        if order.buyer != profile_cur:
            messages.add_message(self.request, messages.WARNING, "订单不属于你")
            return render(self.request, 'comment.html', locals())
        if order.state != 4:
            messages.add_message(self.request, messages.WARNING, "订单不处于待评价状态")
            return render(self.request, 'comment.html', locals())
        models.Comment.objects.create(order=order, stars=self.request.POST['stars'],
                                      comment_text=self.request.POST['comment_text'])
        order.state = 5
        order.save()
        order.product.state = 5
        order.product.save()
        messages.add_message(self.request, messages.SUCCESS, "评价成功")
        return redirect('/myorder')

class Check_control:
    def __init__(self, request):
        self.request = request
        self.user = request.user
        if request.user.is_authenticated:
            self.profile = models.Profile.objects.get(user=request.user)
        self.TheTimeOfNow = datetime.now()

    def check(self):
        TheTimeOfNow = datetime.now()
        if not self.request.user.is_authenticated:
            return redirect('/login')
        username = self.request.user.username
        profile_cur = models.Profile.objects.get(user=self.request.user)
        if profile_cur.usertype != 1:
            messages.add_message(self.request, messages.WARNING, "你不是管理员")
            return redirect('/')
        if self.request.method == 'POST':
            check_form = forms.CheckForm(self.request.POST)
            if not check_form.is_valid():
                messages.add_message(self.request, messages.INFO, "请检查输入字段的内容")
                return redirect('/check')
            try:
                product = models.Product.objects.get(id=self.request.POST['product_id'])
            except:
                messages.add_message(self.request, messages.WARNING, "商品编号处理异常")
                return redirect('/check')
            if product.state != -2 and product.state != -1 and product.state != 0:
                messages.add_message(self.request, messages.WARNING, "此商品已被购买")
                return redirect('/check')
            state_cur = self.request.POST['state']
            if state_cur == '0':
                product.state = 0
                product.save()
                messages.add_message(self.request, messages.SUCCESS, "通过")
            if state_cur == '1':
                product.state = -2
                product.save()
                messages.add_message(self.request, messages.SUCCESS, "不通过")

        all_products = models.Product.objects.filter(state=-1).order_by("-id")
        paginator_cur = paginator.Paginator(all_products, 5)
        p = self.request.GET.get('p')
        try:
            products = paginator_cur.page(p)
        except paginator.PageNotAnInteger:
            products = paginator_cur.page(1)
        except paginator.EmptyPage:
            products = paginator_cur.page(paginator_cur.num_pages)
        return render(self.request, 'check.html', locals())

    def checkall(self):
        TheTimeOfNow = datetime.now()
        if not self.request.user.is_authenticated:
            return redirect('/login')
        username = self.request.user.username
        profile_cur = models.Profile.objects.get(user=self.request.user)
        if profile_cur.usertype != 1:
            messages.add_message(self.request, messages.WARNING, "你不是管理员")
            return redirect('/')
        if self.request.method == 'POST':
            check_form = forms.CheckForm(self.request.POST)
            if not check_form.is_valid():
                messages.add_message(self.request, messages.INFO, "请检查输入字段的内容")
                return redirect('/checkall')
            try:
                product = models.Product.objects.get(id=self.request.POST['product_id'])
            except:
                messages.add_message(self.request, messages.WARNING, "商品编号处理异常")
                return redirect('/checkall')
            if product.state != -2 and product.state != -1 and product.state != 0:
                messages.add_message(self.request, messages.WARNING, "此商品已被购买")
                return redirect('/checkall')
            state_cur = self.request.POST['state']
            if state_cur == '0':
                product.state = 0
                product.save()
                messages.add_message(self.request, messages.SUCCESS, "通过")
            if state_cur == '1':
                product.state = -2
                product.save()
                messages.add_message(self.request, messages.SUCCESS, "不通过")

        all_products = models.Product.objects.all().order_by("-id")
        paginator_cur = paginator.Paginator(all_products, 5)
        p = self.request.GET.get('p')
        try:
            products = paginator_cur.page(p)
        except paginator.PageNotAnInteger:
            products = paginator_cur.page(1)
        except paginator.EmptyPage:
            products = paginator_cur.page(paginator_cur.num_pages)
        return render(self.request, 'checkall.html', locals())

from django.shortcuts import render
from mainsite import models, forms
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core import paginator
from django.views.decorators.csrf import csrf_exempt
from mainsite import controllers
from mainsite import Interfaces

# 登录，属于“登录”用例
def login(request):
    return controllers.Account_control(request).login()

# 注销
@login_required(login_url='/login/')
def logout(request):
    return controllers.Account_control(request).logout()

# 注册
def register(request):
    return controllers.Account_control(request).register()

# 生成订单，属于“购买商品”用例
@login_required(login_url='/login/')
def order_add(request):
    return controllers.Order_control(request).add()

# 取消订单，属于“购买商品”用例，非核心场景
@login_required(login_url='/login/')
def order_remove(request):
    return controllers.Order_control(request).remove()

# 添加商品，属于“添加、修改商品”用例
@login_required(login_url='/login/')
def product_add(request):
    return controllers.Product_control(request).add()

# 修改商品，属于“添加、修改商品”用例
@login_required(login_url='/login/')
def product_modify(request, product_id):
    return controllers.Product_control(request).modify(product_id)

# 修改个人信息
@login_required(login_url='/login/')
def profile_modify(request):
    return controllers.Account_control(request).modify()

# 修改密码
@login_required(login_url='/login/')
def change_password(request):
    return controllers.Account_control(request).change_password()

# 删除商品，属于“添加、修改商品”，非核心场景
@login_required(login_url='/login/')
def product_remove(request):
    return controllers.Product_control(request).remove()

# 发送支付信息到第三方平台，属于“购买商品”用例
@login_required(login_url='/login/')
def pay(request):
    return controllers.Payment(request).pay(Interfaces.Billing())

# 接收第三方支付平台返回信息，成功场景
@csrf_exempt
def pay_finish(request):
    return controllers.Payment(request).pay_finish(Interfaces.Billing())

# 接受第三方支付平台返回信息，非核心场景
@csrf_exempt
def pay_cancel(request):
    return controllers.Payment(request).pay_cancel(Interfaces.Billing())

# 评论商品，属于“评论商品”用例
@login_required(login_url='/login/')
def comment(request, order_id):
    return controllers.Comment_control(request).comment(order_id)

# 审核尚未审核的商品，属于“审核商品”用例
@login_required(login_url='/login/')
def check(request):
    return controllers.Check_control(request).check()

# 审核所有商品，属于“审核商品”用例
@login_required(login_url='/login/')
def checkall(request):
    return controllers.Check_control(request).checkall()

# 发送邮件到邮箱，属于“验证身份”用例
@login_required(login_url='/login/')
def college_authenticate(request):
    return controllers.College_authenticate_control(request).authenticate(Interfaces.Email_sending())

# 输入key，确认验证通过，属于“验证身份”用例
@login_required(login_url='/login/')
def college_authenticate_confirm(request):
    return controllers.College_authenticate_control(request).authenticate_confirm()

# 发送绑定信息到第三方支付平台
@login_required(login_url='/login/')
def bind_payment(request):
    return controllers.Bind_payment_control(request).bind()

# 输入key，确认绑定支付账号验证通过
@login_required(login_url='/login/')
def bind_payment_confirm(request):
    return controllers.Bind_payment_control(request).bind_confirm()

# ----------------------------------------------------------------------
# 接下来并不是我们所分工需要实现的用例，因此直接采取函数实现
# ----------------------------------------------------------------------

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
    return render(request, 'index.html', locals())

@login_required(login_url='/login/')
def userinfo(request):
    TheTimeOfNow = datetime.now()
    messages.get_messages(request)
    if request.user.is_authenticated:
        username = request.user.username
        userinfo = models.Profile.objects.get(user = request.user)
        profile_cur = models.Profile.objects.get(user=request.user)
    return render(request, 'userinfo.html', locals())

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

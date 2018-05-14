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

# Create your views here.

def index(request, pid = None, del_pass = None):
    TheTimeOfNow = datetime.now()
    if request.user.is_authenticated:
        username = request.user.username
        profile_cur = models.Profile.objects.get(user=request.user)
    messages.get_messages(request)
    return render(request,'index.html',locals())

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

@login_required(login_url='/login/')
def userinfo(request):
    TheTimeOfNow = datetime.now()
    if request.user.is_authenticated:
        username = request.user.username
        userinfo = models.Profile.objects.get(user = request.user)
    return render(request, 'userinfo.html', locals())

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
                paypassword = request.POST['paypassword']
                paypassword_confirm = request.POST['paypassword_confirm']
                if confirm_password == register_password and paypassword == paypassword_confirm:
                    user_exist = User.objects.filter(username = register_name).exists()
                    if user_exist:
                        messages.add_message(request, messages.WARNING, "此用户名已被注册")
                    else:
                        current_user = User.objects.create_user(register_name, '', register_password)
                        models.Profile.objects.create(user = current_user, id = current_user.id, paypassword = paypassword)
                        messages.add_message(request, messages.SUCCESS, "注册成功")
                        return redirect('/')
                else:
                    messages.add_message(request, messages.WARNING, "两次输入的密码不符")
            else:
                messages.add_message(request, messages.INFO, "请检查输入字段的内容")
        else:
            login_form = forms.LoginForm()
        return render(request,'register.html',locals())

@csrf_exempt
def pay(request):
    if request.method == 'POST':
        payer = request.POST['payer']
        receiver = request.POST['receiver']
        amount = request.POST['amount']
        order = request.POST['order']
        payer_cur = models.Profile.objects.get(user = User.objects.get(username = payer))
        receiver_cur = models.Profile.objects.get(user = User.objects.get(username = receiver))
        try:
            payment = models.Payment.objects.get(order = order)
        except:
            models.Payment.objects.create(payer = payer_cur, receiver = receiver_cur, amount = amount, order = order)
            payment = models.Payment.objects.get(order=order)
        payment.state = 0
        payment.save()

        return render(request, "pay.html", locals())

@login_required(login_url='/login/')
def pay_confirm(request, payment_id):
    TheTimeOfNow = datetime.now()
    if request.user.is_authenticated:
        username = request.user.username
    profile_cur = models.Profile.objects.get(user = request.user)
    if request.method == 'POST':
        confirm_form = forms.ConfirmForm(request.POST)
        if not confirm_form.is_valid():
            messages.add_message(request, messages.INFO, "请检查输入字段的内容")
            return render(request, "pay_confirm.html", locals())
        user_cur = authenticate(username=username, password=request.POST['password'])
        if user_cur is None:
            messages.add_message(request, messages.WARNING, "密码错误")
            return render(request, 'pay_confirm.html', locals())
        try:
            payment = models.Payment.objects.get(id = payment_id)
        except:
            messages.add_message(request, messages.WARNING, "订单不存在")
            return render(request, 'pay_confirm.html', locals())
        if payment.payer != profile_cur:
            messages.add_message(request, messages.WARNING, "订单不属于你")
            return render(request, 'pay_confirm.html', locals())
        if payment.state != 0:
            messages.add_message(request, messages.WARNING, "订单不处于待付款状态")
            return render(request, 'pay_confirm.html', locals())
        state_cur = request.POST['state']
        if state_cur == "0":
            url = 'http://127.0.0.1:8086/pay_finish'
        if state_cur == "1":
            url = 'http://127.0.0.1:8086/pay_cancel'
        d = {
            'token': 'SKAMcjkso987UjPaqmcj012Kjidusjnb',
            'order_id': payment.order,
        }
        try:
            r = requests.post(url, data=d)
        except:
            messages.add_message(request, messages.WARNING, "系统繁忙")
            return render(request, 'pay_confirm.html', locals())

        messages.add_message(request, messages.SUCCESS, "成功")
        payment.state = 1
        payment.save()

    return render(request, "pay_confirm.html", locals())

@csrf_exempt
def email_binding(request):
    if request.method == 'POST':
        email = request.POST['email']
        key = request.POST['key']
        try:
            email_binding = models.EmailBinding.objects.get(email = email)
        except:
            models.EmailBinding.objects.create(email = email, key = key)
            email_binding = models.Payment.objects.get(email=email)
        email_binding.key = key
        email_binding.save()

        return render(request, "email_binding.html", locals())

def email_look(request):
    TheTimeOfNow = datetime.now()
    email = request.GET.get('email')
    if email is None:
        return redirect('/')
    if request.user.is_authenticated:
        username = request.user.username
    try:
        email_cur = models.EmailBinding.objects.get(email=email)
    except:
        messages.add_message(request, messages.WARNING, "此邮箱不存在")
        return render(request, 'email_look.html', locals())
    key = email_cur.key
    return render(request, 'email_look.html', locals())

@csrf_exempt
def pay_binding(request):
    is_success = "False"
    if request.method == 'POST':
        payment = request.POST['payment']
        key = request.POST['key']
        trade_profile = request.POST['profile']
        try:
            user_binding = User.objects.get(username = payment)
        except:
            return render(request, "pay_binding.html", locals())
        profile_binding = models.Profile.objects.get(user = user_binding)
        try:
            pay_binding = models.Binding.objects.get(profile = profile_binding, trade_profile = trade_profile)
        except:
            models.Binding.objects.create(profile = profile_binding, trade_profile = trade_profile, key = key)
            pay_binding = models.Payment.objects.get(profile = profile_binding, trade_profile = trade_profile)
        pay_binding.key = key
        pay_binding.save()

        return render(request, "pay_binding.html", locals())

@login_required(login_url='/login/')
def bind_look(request):
    TheTimeOfNow = datetime.now()
    if request.user.is_authenticated:
        username = request.user.username
    profile_cur = models.Profile.objects.get(user=request.user)

    bindings = models.Binding.objects.filter(profile=profile_cur)

    return render(request, 'bind_look.html', locals())
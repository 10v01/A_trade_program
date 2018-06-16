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
from mainsite import controllers

class IBillingSystem:
    def send_payment_info(self, order, method):
        pass

class BillingSystem(IBillingSystem):
    def send_payment_info(self, order, method):
        r = Billing_for_testpay().send_payment_info(order)
        return r

class Billing_for_testpay:
    def send_payment_info(self, order):
        d = {
            'payer': order.buyer.BoundPayment,
            'receiver': order.product.seller.BoundPayment,
            'amount': order.product.price,
            'order': order.id,
        }
        r = Testpay_interface().send_payment_info(d)
        return r

class Testpay_interface:
    def send_payment_info(self, d):
        url = 'http://127.0.0.1:10086/pay'
        try:
            r = requests.post(url, data=d)
            return r
        except:
            return None

class Pay_result_testpay:
    def __init__(self, request):
        self.request = request

    def success(self):
        if self.request.method != "POST":
            return redirect('/')
        pay_finish_form = forms.PayFinish(self.request.POST)
        if not pay_finish_form.is_valid():
            return redirect('/')
        token = self.request.POST['token']
        order_id = self.request.POST['order_id']
        if token != "SKAMcjkso987UjPaqmcj012Kjidusjnb":
            return redirect('/')
        try:
            order_cur = models.Order.objects.get(id=order_id)
        except:
            return redirect('/')
        controllers.Pay_result_control().pay_finish(order_cur)
        return render(self.request, 'pay_finish.html', locals())

    def cancel(self):
        if self.request.method != "POST":
            return redirect('/')
        pay_cancel_form = forms.PayCancel(self.request.POST)
        if not pay_cancel_form.is_valid():
            return redirect('/')
        token = self.request.POST['token']
        order_id = self.request.POST['order_id']
        if token != "SKAMcjkso987UjPaqmcj012Kjidusjnb":
            return redirect('/')
        try:
            order_cur = models.Order.objects.get(id=order_id)
        except:
            return redirect('/')
        controllers.Pay_result_control().pay_cancel(order_cur)
        return render(self.request, 'pay_cancel.html', locals())

class IEmail_sending:
    def send_email(self, email, key):
        pass

class Email_sending(IEmail_sending):
    def send_email(self, email, key):
        url = 'http://127.0.0.1:10086/email_binding'
        d = {
            'email': email,
            'key': key,
        }
        try:
            r = requests.post(url, data=d)
            return 0
        except:
            return None

class IComment_manage:
    def submit(self):
        pass
class Comment_manage(IComment_manage):
    def __init__(self, request):
        self.request = request
        self.order = models.Order.objects.get(id = request.POST['order_id'])
    def submit(self):
        comment=models.Comment.objects.create(order=self.order, stars=self.request.POST['stars'],comment_text=self.request.POST['comment_text'])

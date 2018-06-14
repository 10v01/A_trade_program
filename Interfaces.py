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

class IBilling:
    def send_payment_info(self, payer, receiver, amount, order_id):
        pass

    def payment_result_success(self, request):
        pass

    def payment_result_cancel(self, request):
        pass

class Billing(IBilling):
    def send_payment_info(self, payer, receiver, amount, order_id):
        url = 'http://127.0.0.1:10086/pay'
        d = {
            'payer': payer,
            'receiver': receiver,
            'amount': amount,
            'order': order_id,
        }
        try:
            r = requests.post(url, data=d)
            return r
        except:
            return None

    def payment_result_success(self, request):
        if request.method != "POST":
            return redirect('/')
        pay_finish_form = forms.PayFinish(request.POST)
        if not pay_finish_form.is_valid():
            return redirect('/')
        token = request.POST['token']
        order_id = request.POST['order_id']
        if token != "SKAMcjkso987UjPaqmcj012Kjidusjnb":
            return redirect('/')
        order_cur = models.Order.objects.get(id=order_id)
        order_cur.state = 2
        order_cur.save()
        order_cur.product.state = 2
        order_cur.product.save()
        return render(request, 'pay_finish.html', locals())

    def payment_result_cancel(self, request):
        if request.method != "POST":
            return redirect('/')
        pay_cancel_form = forms.PayCancel(request.POST)
        if not pay_cancel_form.is_valid():
            return redirect('/')
        token = request.POST['token']
        order_id = request.POST['order_id']
        if token != "SKAMcjkso987UjPaqmcj012Kjidusjnb":
            return redirect('/')
        order_cur = models.Order.objects.get(id=order_id)
        order_cur.state = 0
        order_cur.save()
        return render(request, 'pay_finish.html', locals())

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

class Isubmit:
    def submit(self):
        pass

class submit(Isubmit):
    def submit(self):
        product = models.Product.objects.get(id=self.request.POST['product_id'])
        product.save()

"""payment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from mainsite import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('login', views.login),
    path('login/', views.login),
    path('logout', views.logout),
    path('logout/', views.logout),
    path('userinfo',views.userinfo),
    path('userinfo/',views.userinfo),
    path('accounts/register', views.register),
    path('accounts/register/', views.register),
    path('pay/', views.pay),
    path('pay', views.pay),
    re_path(r'^pay/(\d+)$', views.pay_confirm),
    path('email_binding', views.email_binding),
    path('email_binding/', views.email_binding),
    path('email_look', views.email_look),
    path('email_look/', views.email_look),
    path('pay_binding', views.pay_binding),
    path('pay_binding/', views.pay_binding),
    path('bind_look', views.bind_look),
    path('bind_look/', views.bind_look),
]

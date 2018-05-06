"""college_second_hand URL Configuration

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
from django.urls import path,re_path
from mainsite import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('logout/', views.logout),
    path('', views.index),
    path('userinfo',views.userinfo),
    path('accounts/register', views.register),
    path('mylist', views.mylist),
    path('mymark', views.mymark),
    path('mycart', views.mycart),
    path('pay', views.pay),
    re_path(r'^product/(\d+)$', views.product, name = "product-url"),
    re_path(r'^pay/(\d+)$', views.pay),
]

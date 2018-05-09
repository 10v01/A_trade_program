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
    path('login', views.login),
    path('login/', views.login),
    path('logout', views.logout),
    path('logout/', views.logout),
    path('', views.index),
    path('userinfo',views.userinfo),
    path('userinfo/',views.userinfo),
    path('accounts/register', views.register),
    path('accounts/register/', views.register),
    path('myorder', views.myorder),
    path('myorder/', views.myorder),
    path('mymark', views.mymark),
    path('mymark/', views.mymark),
    path('pay', views.pay),
    path('pay/', views.pay),
    re_path(r'^product/(\d+)$', views.product, name = "product-url"),
    path('order_add', views.order_add),
    path('order_add/', views.order_add),
    path('order_remove', views.order_remove),
    path('order_remove/', views.order_remove),
    path('product_add', views.product_add),
    path('product_add/', views.product_add),
    path('myproduct', views.myproduct),
    path('myproduct/', views.myproduct),
    re_path(r'^product_modify/(\d+)$', views.product_modify),
    path('mark_add', views.mark_add),
    path('mark_add/', views.mark_add),
    path('mark_remove', views.mark_remove),
    path('mark_remove/', views.mark_remove),
    path('product_remove', views.product_remove),
    path('product_remove/', views.product_remove),
    path('search', views.search),
]

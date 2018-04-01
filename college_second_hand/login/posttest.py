# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators import csrf
from django.template.loader import get_template
from django.http import HttpResponse

def search_post(request):
    ctx = {}
    template = get_template('post.html')
    html = template.render(locals())
    #if request.POST:
    #    ctx['rlt'] = request.POST['q']
    return render(request, "post.html", ctx)
    return HttpResponse(html)
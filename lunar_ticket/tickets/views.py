# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from datetime import date

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from models import *
from forms import OrderForm
from django.views import generic
from django.core.urlresolvers import reverse


# Create your views here.

STATUSES = {
    'today': u'Задачи на сегодня',
    'someday': u'Все задачи' ,
    'fixed': u'Выпоненые задачи'
    }
ACTION_DELETE = {'delete': u"Удалить выбраные", }


@login_required
def index(request):
    template = loader.get_template('tickets/index.html')
    context = RequestContext(request, {
        'message': 'valera vvvv'
    })
    return HttpResponse(template.render(context))

def play_detail(request):
    template = loader.get_template('tickets/detail.html')
    print 'okookokokok'
    context = RequestContext(request)
    return HttpResponse(template.render(context=context))
def plays(request):
    template = loader.get_template('tickets/index.html')
    print 'okookokokok'
    context = RequestContext(request)
    return HttpResponse(template.render(context=context))
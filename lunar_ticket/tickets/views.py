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
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
from month_calendar import WorkoutCalendar
from datetime import date


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
    my_workouts = Scheduler.objects.all()
    today = date.today()

    context = RequestContext(request, {
        'calendar': calendar(request, today.year, today.month),
    })
    return HttpResponse(template.render(context))

def play_detail(request, pk):
    template = loader.get_template('tickets/detail.html')
    context = RequestContext(request, {
        'scheduler': Scheduler.objects.get(pk=pk),
        'pk': pk,

    })
    return HttpResponse(template.render(context))

def plays(request, date):
    template = loader.get_template('tickets/plays.html')
    context = RequestContext(request, {
        'plays': Play.objects.all(),
    })
    return HttpResponse(template.render(context=context))

def calendar(request, year, month):
  my_workouts = Scheduler.objects.order_by('date').filter(
    date__year=year, date__month=month
  )
  cal = WorkoutCalendar(my_workouts).formatmonth(year, month)
  return mark_safe(cal)
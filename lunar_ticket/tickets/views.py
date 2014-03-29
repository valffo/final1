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
from dateutil.relativedelta import relativedelta
from datetime import datetime
from django.contrib.auth.models import User, Group
from django.db.models import Count, Min, Sum, Avg

# Create your views here.

STATUSES = {
    'today': u'Задачи на сегодня',
    'someday': u'Все задачи' ,
    'fixed': u'Выпоненые задачи'
    }
ACTION_DELETE = {'delete': u"Удалить выбраные", }


@login_required
def index(request, month):
    template = loader.get_template('tickets/index.html')
    my_workouts = Scheduler.objects.all()
    if (month):
        calendar_date = datetime.strptime(month, "%Y%m")
    else:
        calendar_date = date.today()
    context = RequestContext(request, {
        'calendar': calendar(request, calendar_date.year, calendar_date.month),
        'next_month': calendar_date + relativedelta(months=+1),
        'prev_month': calendar_date + relativedelta(months=-1),
    })
    return HttpResponse(template.render(context))

def play_detail(request, pk):
    template = loader.get_template('tickets/detail.html')
    scheduler = Scheduler.objects.get(pk=pk)
    orders = Order.objects.values('ticket').filter(scheduler=scheduler)\
        .annotate(count_ticket=Sum('count'))
    context = RequestContext(request, {
        'scheduler': scheduler,
        'orders': orders,
        'tickets': Ticket.objects.filter(scheduler=scheduler)

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
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
    orders = Order.objects.values('ticket').filter(scheduler=scheduler) \
        .annotate(count_ticket=Sum('count'))

    availables = {x['ticket']: x['count_ticket'] for x in orders}
    context = RequestContext(request, {
        'scheduler': scheduler,
        'orders': orders,
        'availables': availables,
        'tickets': Ticket.objects.filter(scheduler=scheduler),
        'form': form_order

    })
    return HttpResponse(template.render(context))


def plays(request, date):
    template = loader.get_template('tickets/plays.html')
    context = RequestContext(request, {
        'plays': Play.objects.all(),
    })
    return HttpResponse(template.render(context=context))


def buy(request):
    #if request.method == 'POST':
        #for ticket_id, count in request.POST.getlist('type'):
        #    order = Order(
        #        scheduler=Scheduler.objects.get(request.POST['scheduler']),
        #        user=User,
        #        count=count,
        #        date_purchase=datetime.date()
        #    )
        #    order.save()
    template = loader.get_template('tickets/cart.html')
    context = RequestContext(request, {
        #'orders': Order.objects.filter(user=User),
        'orders': request.POST.getlist('type[]'),
        #'orders': request.POST['scheduler'],

    })
    return HttpResponse(template.render(context))
    return HttpResponseRedirect(reverse('cart'))

def cart(request):
    template = loader.get_template('tickets/detail.html')
    context = RequestContext(request, {
        'orders': Order.objects.filter(user=User),
    })
    return HttpResponse(template.render(context))

def form_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            for ticket_id, count in request.POST.list['']:
                order = Order(
                    scheduler=Scheduler.objects.get(request.POST['scheduler']),
                    user=User,
                    count=count,
                    date_purchase=datetime.date()
                )
                order.save()
            return HttpResponseRedirect(reverse('home', kwargs={'pk': order.scheduler.id, }))

    return OrderForm()


def calendar(request, year, month):
    my_workouts = Scheduler.objects.order_by('date').filter(
        date__year=year, date__month=month
    )
    cal = WorkoutCalendar(my_workouts).formatmonth(year, month)
    return mark_safe(cal)


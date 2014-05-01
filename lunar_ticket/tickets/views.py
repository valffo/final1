# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.template import RequestContext, loader
from datetime import date

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from models import *
from forms import *
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
    scheduler = Scheduler.objects.get(pk=pk)
    if (request.user.groups.filter(name='carrier').count):
        template = loader.get_template('tickets/carrier.html')
        form = CurrierForm(scheduler=scheduler, request=request).as_table()
    else:
        template = loader.get_template('tickets/detail.html')
        form = OrderForm(scheduler=scheduler, request=request).as_table()


    context = RequestContext(
        request,
        {
            'scheduler': scheduler,
            'form': form
        }
    )

    return StreamingHttpResponse(template.render(context))


def plays(request, date):
    template = loader.get_template('tickets/plays.html')
    context = RequestContext(request, {
        'plays': Play.objects.all(),
    })
    return HttpResponse(template.render(context=context))


def cart(request, pk=None):
    template = loader.get_template('tickets/cart.html')
    context = RequestContext(request, {
        'orders': Order.objects.filter(user=User),
        'pk': pk
    })
    return HttpResponse(template.render(context))


def buy(request):
    pkkk=0
    if request.method == 'POST':
        scheduler = Scheduler.objects.get(pk=request.POST['scheduler'])
        form = OrderForm(request.POST, scheduler=scheduler, request=request)
        if form.is_valid():
            for ticket in form.changed_data:
                ticket_id = ticket.split('_')[1]
                #return StreamingHttpResponse(ticket+ '!!!' + ticket_id)
                #print ticket_type
                order = Order(
                    scheduler=scheduler,
                    ticket=Ticket.objects.get(pk=ticket_id),
                    user=User.objects.get(pk=request.user.id),
                    count=request.POST[ticket],
                    date_purchase=datetime.now()
                )
                order.save()
                pkkk = order.id
    return HttpResponseRedirect(reverse('detail', kwargs={'pk': request.POST['scheduler'], }))

def pay(request):
    if request.method == 'POST':
        scheduler = Scheduler.objects.get(pk=request.POST['scheduler'])
        form = CurrierForm(request.POST, scheduler=scheduler, request=request)
        if form.is_valid():
            for order_post in form.changed_data:
                order_id = order_post.split('_')[1]
                # return StreamingHttpResponse(request.POST[order_post] + ' === ' + order_post+ '!!!' + order_id)
                # print ticket_type
                order = Order.objects.get(pk=order_id)
                order.count = request.POST[order_post]
                order.pay_status = 1
                order.save()
                pkkk = order.id
    return HttpResponseRedirect(reverse('detail', kwargs={'pk': request.POST['scheduler'], }))

def calendar(request, year, month):
    my_workouts = Scheduler.objects.order_by('date').filter(
        date__year=year, date__month=month
    )
    cal = WorkoutCalendar(my_workouts).formatmonth(year, month)
    return mark_safe(cal)


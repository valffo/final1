# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
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
    context = RequestContext(
        request,
        {
            'scheduler': scheduler,
            'form': OrderForm(scheduler=scheduler).as_table()
        }
    )

    return StreamingHttpResponse(template.render(context))


def plays(request, date):
    template = loader.get_template('tickets/plays.html')
    context = RequestContext(request, {
        'plays': Play.objects.all(),
    })
    return HttpResponse(template.render(context=context))


#def buy(request):
#    #if request.method == 'POST':
#        #for ticket_id, count in request.POST.getlist('type'):
#        #    order = Order(
#        #        scheduler=Scheduler.objects.get(request.POST['scheduler']),
#        #        user=User,
#        #        count=count,
#        #        date_purchase=datetime.date()
#        #    )
#        #    order.save()
#    template = loader.get_template('tickets/cart.html')
#    context = RequestContext(request, {
#        #'orders': Order.objects.filter(user=User),
#        'orders': request.POST.getlist('type[]'),
#        #'orders': request.POST['scheduler'],
#
#    })
#    return HttpResponse(template.render(context))
#    return HttpResponseRedirect(reverse('cart'))


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
        form = OrderForm(request.POST, scheduler=scheduler)
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
    return HttpResponseRedirect(reverse('cart', kwargs={'pk': pkkk, }))

def calendar(request, year, month):
    my_workouts = Scheduler.objects.order_by('date').filter(
        date__year=year, date__month=month
    )
    cal = WorkoutCalendar(my_workouts).formatmonth(year, month)
    return mark_safe(cal)


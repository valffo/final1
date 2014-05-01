# -*- coding: utf-8 -*-
from django import forms
from models import *
from django.db.models import Count, Min, Sum, Avg
from django.utils.safestring import mark_safe

class CurrierForm(forms.Form):
    def __init__(self, *args, **kwargs):
        request = kwargs.get('request')
        scheduler = kwargs.get('scheduler')
        del kwargs['request']
        del kwargs['scheduler']
        super(CurrierForm, self).__init__(*args, **kwargs)
        orders = Order.objects.filter(scheduler=scheduler)

        self.fields['scheduler'] = forms.IntegerField(widget=forms.HiddenInput(), initial=scheduler.id)
        for order in orders:
            attrs = {}
            label = mark_safe('</td><td>'.join(
                [
                    str(order.scheduler),
                    str(order.user.username),
                    str(order.ticket.ticket_type.title),
                    str(order.date_purchase),
                    str(order.count),
                    str(order.count * order.ticket.cost),
                    'payed' if order.pay_status else 'not payed'


                ]
            ))
            if (order.pay_status):
                attrs={'disabled': 'disabled'}
            # self.fields[''.join(['order_', str(order.id)])] = forms.BooleanField(label=label)
            self.fields[''.join(['order_', str(order.id)])] = forms.IntegerField(label=label, required=False, widget=forms.NumberInput(attrs=attrs))

class OrderForm(forms.Form):

    DATE_INPUT_FORMATS = 'd.m.Y'

    def __init__(self, *args, **kwargs):
        request = kwargs.get('request')
        options = self.get_form_options(kwargs.get('scheduler'))
        del kwargs['request']
        del kwargs['scheduler']
        super(OrderForm, self).__init__(*args, **kwargs)
        user = User.objects.get(pk=request.user.id)

        for ticket in options['tickets']:
            label = mark_safe('</td><td>'.join(
                [
                    ticket.ticket_type.title,
                    str(ticket.cost),
                    str(ticket.ticket_type.count - int(options['availables'].get(ticket.id, 0))),
                    str(self.get_order_count_by_ticket(user, options['scheduler'], ticket))
                ]
            ))
            self.fields[''.join(['ticket_', str(ticket.id)])] = forms.IntegerField(
                label=label,
                max_value=ticket.ticket_type.count - int(options['availables'].get(ticket.id, 0)),
                min_value=0,
                initial=0
            )

        self.fields['scheduler'] = forms.IntegerField(widget=forms.HiddenInput(), initial=options['scheduler'].id)

    def get_form_options(self, scheduler):

        orders = Order.objects.values('ticket').filter(scheduler=scheduler) \
            .annotate(count_ticket=Sum('count'))

        availables = {x['ticket']: x['count_ticket'] for x in orders}
        return {
            'scheduler': scheduler,
            'availables': availables,
            'tickets': Ticket.objects.filter(scheduler=scheduler),
        }

    def get_order_count_by_ticket(self, user, scheduler, ticket):
        return int(Order.objects.filter(user=user, scheduler=scheduler, ticket=ticket).aggregate(Sum('count'))['count__sum'] or 0)


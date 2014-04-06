# -*- coding: utf-8 -*-
from django import forms
from models import *
from django.db.models import Count, Min, Sum, Avg

class OrderForm(forms.Form):

    DATE_INPUT_FORMATS = 'd.m.Y'

    def __init__(self, *args, **kwargs):
        options = self.get_form_options(kwargs.get('scheduler'))
        #options = kwargs.get('options')
        del kwargs['scheduler']
        super(OrderForm, self).__init__(*args, **kwargs)
        for ticket in options['tickets']:
            label = ' '.join(
                [
                    ticket.ticket_type.title,
                    ' Cost: ', str(ticket.cost), u' рублей.',
                    ' Available: ', str(ticket.ticket_type.count - int(options['availables'].get(ticket.id, 0)))
                ]
            )
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




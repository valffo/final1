# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Min, Sum, Avg

class Play(models.Model):
    title = models.CharField(max_length=255)
    describe = models.TextField()
    def __str__(self):
        return ''.join([self.title.encode('utf8'), ' (#ID: ', str(self.id), ')', ])

class Scheduler(models.Model):
    #reporter = models.ForeignKey(Reporter)
    #publications = models.ManyToManyField(Play)
    play = models.ForeignKey(Play)
    date = models.DateField()
    time = models.TimeField()
    def __str__(self):
        return ' '.join([self.date.strftime('%d.%m.%Y'), self.time.strftime('%H:%M'), str(self.play)])
    def get_absolute_url(self):
        return reverse('detail', args=[self.id])


class TicketType(models.Model):
    title = models.CharField(max_length=100)
    count = models.IntegerField()
    def __str__(self):
        return ' '.join([self.title])

class Ticket(models.Model):
    scheduler = models.ForeignKey(Scheduler)
    ticket_type = models.ForeignKey(TicketType)
    cost = models.BigIntegerField()

    def available(self):
        count = Order.objects.values('ticket').filter(scheduler=self.scheduler, ticket=self) \
            .annotate(count_ticket=Sum('count'))
        return self.ticket_type.count - count[0].get('count_ticket', 0)


    def __str__(self):
        return ' '.join([str(self.scheduler), 'for', str(self.ticket_type), 'for', str(self.cost)])


class Order(models.Model):
    user = models.ForeignKey(User)
    scheduler = models.ForeignKey(Scheduler)
    ticket = models.ForeignKey(Ticket)
    count = models.IntegerField()
    date_purchase = models.DateTimeField()
    pay_status = models.IntegerField(default=0)

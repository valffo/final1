# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

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

class TicketType(models.Model):
    title = models.CharField(max_length=100)
    count = models.IntegerField()
    def __str__(self):
        return ' '.join([self.title])

class Ticket(models.Model):
    play = models.ForeignKey(Scheduler)
    ticket_type = models.ForeignKey(TicketType)
    cost = models.BigIntegerField()

class Order(models.Model):
    user = models.ForeignKey(User)
    scheduler = models.ForeignKey(Scheduler)
    ticket = models.ForeignKey(Ticket)
    count = models.IntegerField()
    date_purchase = models.DateTimeField()

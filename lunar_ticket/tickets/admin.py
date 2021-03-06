# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from models import Play, Scheduler, Ticket,TicketType, Order
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _

admin.site.unregister(User)

class PlayInline(admin.TabularInline):
    model = Play
    raw_id_fields = ("title",)

# Register your models here.
class PlayAdmin(admin.ModelAdmin):
    # ...
    list_display = ('title', 'describe',)
    list_filter = ['title', ]
    search_fields = ['title', 'describe']
admin.site.register(Play, PlayAdmin)

class SchedulerAdmin(admin.ModelAdmin):
    # ...
    list_select_related = ('play', )
    list_select_related = ('tickets', )
    list_display = ('get_play', 'date', 'time')
    list_filter = ['date',]
    search_fields = ['date', 'play']
    def get_play(self, obj):
        return obj.play.title
    get_play.short_description = 'Plays'

admin.site.register(Scheduler, SchedulerAdmin)

class TicketTypeAdmin(admin.ModelAdmin):
    # ...
    list_display = ('title', 'count',)
    list_filter = ['title',]
    search_fields = ['title',]

admin.site.register(TicketType, TicketTypeAdmin)

class TicketAdmin(admin.ModelAdmin):
    list_display = ('scheduler', 'ticket_type', 'cost')
    list_filter = ['ticket_type']
admin.site.register(Ticket, TicketAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'scheduler', 'ticket', 'count', 'date_purchase')
    list_filter = ['user', 'scheduler']

admin.site.register(Order, OrderAdmin)

class RegUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_superuser', 'is_active',)

admin.site.register(User, RegUserAdmin)

class DomainAdmin(admin.ModelAdmin):
    filter_horizonal = ('users',)


from django.conf.urls import patterns, url
import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^(?P<month>(\d*))$', views.index, name='home'),
    url(r'^plays/$', views.plays, name='plays'),
    url(r'^detail/(?P<pk>\d+)/$', views.play_detail, name='detail'),
    url(r'^buy$', views.buy, name='buy'),
    url(r'^pay$', views.pay, name='pay'),
    url(r'^report/(?P<pk>\d+)/$', views.report, name='report'),
    url(r'^cart(?P<pk>\d+)/$', views.cart, name='cart'),
)
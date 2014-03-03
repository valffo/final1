from django.conf.urls import patterns, url
from tickets import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    # ex: /tickets/
    url(r'^(?P<status>(today|someday|fixed))/$', views.index, name='tasks_index'),
    url(r'^(?P<pk>\d+)/detail/$', login_required(views.DetailView.as_view()), name='detail'),
    url(r'^do_action/$', views.do_action, name='do_action'),
    url(r'^add/$', views.add, name='add'),
    url(r'^create/$', views.add, name='create'),
)
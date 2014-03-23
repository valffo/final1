from django.conf.urls import patterns, url
import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', views.index, name='home'),
    url(r'^plays/$', views.plays, name='plays'),
    url(r'^detail/(?P<pk>\d+)/$', views.play_detail, name='detail'),
)

    # ex: /tickets/
    #url(r'^(?P<status>(today|someday|fixed))/$', views.index, name='tasks_index'),
    #url(r'^(?P<pk>\d+)/detail/$', login_required(views.DetailView.as_view()), name='detail'),
    #url(r'^do_action/$', views.do_action, name='do_action'),
    #url(r'^add/$', views.add, name='add'),
    #url(r'^create/$', views.add, name='create'),
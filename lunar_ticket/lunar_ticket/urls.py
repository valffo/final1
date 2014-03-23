from django.conf.urls import patterns, include, url
from django.conf import settings
from registration.forms import RegistrationFormUniqueEmail
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^accounts/', include('registration.urls')),
    url(r'^accounts/profile', TemplateView.as_view(template_name='index.html')),
    #Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^blog/' , include('blog.urls')),
    url(r'', include('tickets.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
)

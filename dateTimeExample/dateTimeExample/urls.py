from django.conf.urls import patterns, include, url
from django.conf import  settings
from django.views.generic import RedirectView
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dateTimeExample.views.home', name='home'),
    # url(r'^dateTimeExample/', include('dateTimeExample.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT}),
    ("^", include("formexample.urls")),
    (r'^.*$', RedirectView.as_view(url='/model_form_v3/')),
)

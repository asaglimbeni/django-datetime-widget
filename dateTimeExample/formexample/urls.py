__author__ = 'asagli'

from django.conf.urls import patterns, url
from formexample.views import *

# Blog patterns.
urlpatterns = patterns("example.views",
                       url("^model_form_v3/$", dateTimeViewBootstrap3,),
                       url("^model_form_v2/$", dateTimeViewBootstrap2,),
                       )

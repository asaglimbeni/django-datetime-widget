from django.db import models

# Create your models here.

from django import forms
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget


# Bootstrap 3

class testFormBootstrap3(forms.Form):
    date_time = forms.DateTimeField(widget=DateTimeWidget(usel10n=True, bootstrap_version=3))
    date = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=3))
    time = forms.TimeField(widget=TimeWidget(usel10n=True, bootstrap_version=3))

# Bootstrap 2

class testFormBootstrap2(forms.Form):
    date_time = forms.DateTimeField(widget=DateTimeWidget(usel10n=True, bootstrap_version=2))
    date = forms.DateField(widget=DateWidget(usel10n=True, bootstrap_version=2))
    time = forms.TimeField(widget=TimeWidget(usel10n=True, bootstrap_version=2))

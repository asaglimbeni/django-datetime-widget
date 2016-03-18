from time import strptime, strftime, mktime
from datetime import datetime, time
from django import forms
from django.db import models
from django.conf import settings
from django.forms import fields
from django.forms.utils import from_current_timezone
from widgets import NewAdminSplitDateTimeWidget
from django.utils import timezone as tz
from django.forms.fields import TimeField
from django.core.validators import MaxValueValidator, MinValueValidator

from pytz import timezone

class NewAdminSplitDateTimeField(fields.MultiValueField):
    def __init__(self, input_date_formats=None, *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        localize = kwargs.get('localize', False)
        all_fields = (
            fields.DateField(input_formats=input_date_formats,
                            localize=localize),
            fields.IntegerField(min_value=1, max_value=12),
            fields.IntegerField(min_value=0, max_value=59),
            fields.ChoiceField(choices=[('AM','AM'),('PM','PM')])
        )
        super(NewAdminSplitDateTimeField, self).__init__(all_fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            if data_list[0] in self.empty_values:
                raise ValidationError(self.error_messages['invalid_date'], code='invalid_date')
            if (data_list[1] in self.empty_values or
                data_list[2] in self.empty_values or
                data_list[3] in self.empty_values):
                raise ValidationError(self.error_messages['invalid_time'], code='invalid_time')
            hour = data_list[1]
            if data_list[3] == 'PM' and data_list[1] != 12:
                hour += 12
            if data_list[3] == 'AM' and data_list[1] == 12:
                hour = 0
            input_time = time(hour, data_list[2])
            date_list = [data_list[0], input_time]
            result = datetime.combine(*date_list)
            return from_current_timezone(result)
        return None

    def strptime(self, value, format):
        return datetime.datetime.strptime(force_str(value), format)
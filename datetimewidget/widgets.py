from django.forms import forms, widgets

__author__ = 'Alfredo Saglimbeni'
import re
import uuid

from django.forms.widgets import  MultiWidget , to_current_timezone, DateTimeInput
from django.utils.translation import ugettext as _
from datetime import datetime
from django.utils import translation

I18N = """
$.fn.datetimepicker.dates['en'] = {
    days: %s,
    daysShort: %s,
    daysMin: %s,
    months: %s,
    monthsShort: %s,
    meridiem: %s,
    suffix: %s,
    today: %s
};
"""

datetimepicker_options = """
    format : '%s',
    startDate : '%s',
    endDate : '%s',
    weekStart : %s,
    daysOfWeekDisabled : %s,
    autoclose : %s,
    startView : %s,
    minView : %s,
    maxView : %s,
    todayBtn : %s,
    todayHighlight : %s,
    minuteStep : %s,
    pickerPosition : '%s',
    showMeridian : %s,
    language : '%s',
"""

dateConversion = {
    'P' : '%p',
    'ss' : '%S',
    'ii' : '%M',
    'hh' : '%H',
    'HH' : '%I',
    'dd' : '%d',
    'mm' : '%m',
    #'M' :  '%b',
    #'MM' : '%B',
    'yy' : '%y',
    'yyyy' : '%Y',
}
class DateTimeWidget(MultiWidget):

    def __init__(self, attrs=None, options=None):
        if attrs is None:
            attrs = {'readonly':''}

        if options is None:
            options = {}

        self.option = ()
        self.option += (options.get('format','dd/mm/yyyy hh:ii'),)
        self.option += (options.get('startDate',''),)
        self.option += (options.get('endDate',''),)
        self.option += (options.get('weekStart','0'),)
        self.option += (options.get('daysOfWeekDisabled','[]'),)
        self.option += (options.get('autoclose','false'),)
        self.option += (options.get('startView','2'),)
        self.option += (options.get('minView','0'),)
        self.option += (options.get('maxView','4'),)
        self.option += (options.get('todayBtn','false'),)
        self.option += (options.get('todayHighlight','false'),)
        self.option += (options.get('minuteStep','5'),)
        self.option += (options.get('pickerPosition','bottom-right'),)
        self.option += (options.get('showMeridian','false'),)

        self.language = options.get('language', 'en')
        self.option += (self.language,)

        pattern = re.compile(r'\b(' + '|'.join(dateConversion.keys()) + r')\b')
        self.dataTimeFormat = self.option[0]
        self.format =  pattern.sub(lambda x: dateConversion[x.group()], self.option[0])

        widgets = (DateTimeInput(attrs=attrs,format=self.format),)

        super(DateTimeWidget, self).__init__(widgets, attrs)

    def value_from_datadict(self, data, files, name):
        date_time = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)
        ]
        try:
            D = to_current_timezone(datetime.strptime(date_time[0], self.format))
        except ValueError:
            return ''
        else:
            return D

    def decompress(self, value):
        if value:
            value = to_current_timezone(value)
            return (value,)
        return (None,)

    def format_output(self, rendered_widgets):
        """
        Given a list of rendered widgets (as strings), it inserts an HTML
        linebreak between them.

        Returns a Unicode string representing the HTML for the whole lot.
        """

        js_options = datetimepicker_options % self.option
        id = uuid.uuid4().hex
        return '<div id="%s"  class="input-append date form_datetime">'\
               '%s'\
               '<span class="add-on"><i class="icon-th"></i></span>'\
               '</div>'\
               '<script type="text/javascript">'\
               '$("#%s").datetimepicker({%s});'\
               '</script>  ' % (id, rendered_widgets[0], id, js_options)

    def _media(self):
        js = ["js/bootstrap-datetimepicker.js"]
        if self.language != 'en':
            js.append("js/locales/bootstrap-datetimepicker.%s.js" % self.language)

        return widgets.Media(
            css={
                'all' : ('css/datetimepicker.css',)
            },
            js=js
        )
    media = property(_media)

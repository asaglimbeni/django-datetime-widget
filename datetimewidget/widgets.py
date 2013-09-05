from django.forms import forms, widgets

__author__ = 'Alfredo Saglimbeni'
import re
import uuid

from django.forms.widgets import  MultiWidget , to_current_timezone, DateTimeInput
from datetime import datetime
from django.utils.formats import get_format, get_language
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
    clearBtn : %s,
    language : '%s',
"""

dateConversiontoPython = {
    'P': '%p',
    'ss': '%S',
    'ii': '%M',
    'hh': '%H',
    'HH': '%I',
    'dd': '%d',
    'mm': '%m',
    #'M':  '%b',
    #'MM': '%B',
    'yy': '%y',
    'yyyy': '%Y',
}

dateConversiontoJavascript = {
    '%M': 'ii',
    '%m': 'mm',
    '%I': 'HH',
    '%H': 'hh',
    '%d': 'dd',
    '%Y': 'yyyy',
    '%y': 'yy',
    '%p': 'P',
    '%S': 'ss'
}

class DateTimeWidget(MultiWidget):

    def to_local(self):
        """
        This method have to be called on every request call, because adapt the datetime format to the user.
        !!! It work only if USE_L10N is set TRUE and localize middleware is active.!!!
        otherwise get_format use the server format.
        """
        pattern = re.compile(r'(?<!\w)(' + '|'.join(dateConversiontoJavascript.keys()) + r')\b')
        self.format = get_format('DATETIME_INPUT_FORMATS')[0]
        if hasattr(self, 'widgets') and self.widgets[0]:
            self.widgets[0].format = self.format
        self.option = (pattern.sub(lambda x: dateConversiontoJavascript[x.group()], self.format),) + self.option[1:]
        self.language = get_language()

    def __init__(self, attrs=None, options=None, usel10n = None):
        if attrs is None:
            attrs = {'readonly':''}

        if options is None:
            options = {}

        self.option = ()
        if usel10n is True:
            self.is_localized = True
            #Use local datetime format Only if USE_L10N is true and middleware localize is active
            self.to_local()
        else:
            pattern = re.compile(r'\b(' + '|'.join(dateConversiontoPython.keys()) + r')\b')
            self.option += (options.get('format','dd/mm/yyyy hh:ii'),)
            self.format = pattern.sub(lambda x: dateConversiontoPython[x.group()], self.option[0])

        self.option += (options.get('startDate',''),)
        self.option += (options.get('endDate',''),)
        self.option += (options.get('weekStart','0'),)
        self.option += (options.get('daysOfWeekDisabled','[]'),)
        self.option += (options.get('autoclose','true'),)
        self.option += (options.get('startView','2'),)
        self.option += (options.get('minView','0'),)
        self.option += (options.get('maxView','4'),)
        self.option += (options.get('todayBtn','false'),)
        self.option += (options.get('todayHighlight','false'),)
        self.option += (options.get('minuteStep','5'),)
        self.option += (options.get('pickerPosition','bottom-right'),)
        self.option += (options.get('showMeridian','false'),)
        self.option += (options.get('clearBtn','true'),)

        self.language = options.get('language', 'en')
        self.option += (self.language,)

        widgets = (DateTimeInput(attrs=attrs, format=self.format),)

        super(DateTimeWidget, self).__init__(widgets, attrs)

    def value_from_datadict(self, data, files, name):

        if self.is_localized:
            #Adapt the format to the user.
            self.to_local()

        date_time = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)
        ]
        try:
            D = to_current_timezone(datetime.strptime(date_time[0], self.format))
        except (ValueError, TypeError), e:
            return ''
        else:
            return D

    def decompress(self, value):

        if self.is_localized:
            #Adapt the format to the user.
            self.to_local()

        if value:
            value = to_current_timezone(value).strftime(self.format)
            return (value,)
        return (None,)

    def format_output(self, rendered_widgets):
        """
        Given a list of rendered widgets (as strings), it inserts an HTML
        linebreak between them.

        Returns a Unicode string representing the HTML for the whole lot.
        """

        if self.is_localized:
            #Adapt the format to the user.
            self.to_local()

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
                'all': ('css/datetimepicker.css',)
            },
            js=js
        )
    media = property(_media)
from django.forms import forms, widgets

__author__ = 'Alfredo Saglimbeni'
import re
import uuid
try:
    from django.forms.widgets import to_current_timezone
except ImportError:
    to_current_timezone = lambda obj: obj # passthrough, no tz support
from django.forms.widgets import MultiWidget, DateTimeInput, DateInput, TimeInput
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
    # 'M':  '%b',
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


BOOTSTRAP_INPUT_TEMPLATE = {2: """
                       <div id="%s"  class="controls input-append date">%s
                        %s
					    <span class="add-on"><i class="icon-th"></i></span>
					    </div>
                       <script type="text/javascript">$("#%s").datetimepicker({%s});</script>
                    """,
                   3: """
                    <div id="%s" class="input-group date">%s
                    %s
					<span class="input-group-addon"><span class="glyphicon glyphicon-th"></span></span>
					</div>
					<script type="text/javascript">
					$("#%s").datetimepicker({%s}).find('input').addClass("form-control");
					</script>
                    """
                  }

CLEAR_BTN_TEMPLATE = {2: """<span class="add-on"><i class="icon-remove"></i></span>""",
                      3: """<span class="input-group-addon"><span class="glyphicon glyphicon-remove"></span></span>"""}

class DateTimeWidget(MultiWidget):
    """
    DateTimeWidget is the corresponding widget for Date filed, it renders only the date section of datetime picker.
    """

    def __init__(self, attrs=None, options=None, usel10n=None, widgets=None, bootstrap_version=None):

        if bootstrap_version in [2,3]:
            self.bootstrap_version = bootstrap_version
        else:
            #default 2 to mantain support to old implemetation of django-datetime-widget
            self.bootstrap_version = 2

        if attrs is None:
            attrs = {'readonly': ''}

        if options is None:
            options = {}

        self.option = ()
        if usel10n is True:
            self.is_localized = True
            # Use local datetime format Only if USE_L10N is true and middleware localize is active
            self.to_local()
        else:
            pattern = re.compile(r'\b(' + '|'.join(dateConversiontoPython.keys()) + r')\b')
            self.option += (options.get('format', 'dd/mm/yyyy hh:ii'),)
            self.format = pattern.sub(lambda x: dateConversiontoPython[x.group()], self.option[0])

        self.option += (options.get('startDate', ''),)
        self.option += (options.get('endDate', ''),)
        self.option += (options.get('weekStart', '0'),)
        self.option += (options.get('daysOfWeekDisabled', '[]'),)
        self.option += (options.get('autoclose', 'true'),)
        self.option += (options.get('startView', '2'),)
        self.option += (options.get('minView', '0'),)
        self.option += (options.get('maxView', '4'),)
        self.option += (options.get('todayBtn', 'false'),)
        self.option += (options.get('todayHighlight', 'false'),)
        self.option += (options.get('minuteStep', '5'),)
        self.option += (options.get('pickerPosition', 'bottom-right'),)
        self.option += (options.get('showMeridian', 'false'),)
        self.option += (options.get('clearBtn', 'true'),)

        # set clearBtn needs for format_output
        self.clearBtn = True if options.get('clearBtn', 'true') == 'true' else False

        self.language = options.get('language', 'en')
        self.option += (self.language,)
        if widgets is None:
            widgets = (DateTimeInput(attrs=attrs, format=self.format),)

        super(DateTimeWidget, self).__init__(widgets, attrs)

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

    def value_from_datadict(self, data, files, name):

        if self.is_localized:
            # Adapt the format to the user.
            self.to_local()

        date_time = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)
        ]
        try:
            D = to_current_timezone(datetime.strptime(date_time[0], self.format))
        except (ValueError, TypeError) as e:
            return ''
        else:
            return D

    def decompress(self, value):

        if self.is_localized:
            # Adapt the format to the user.
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
            # Adapt the format to the user.
            self.to_local()

        js_options = datetimepicker_options % self.option

        id = uuid.uuid4().hex
   
        return BOOTSTRAP_INPUT_TEMPLATE[self.bootstrap_version] % (id, rendered_widgets[0], CLEAR_BTN_TEMPLATE[ self.bootstrap_version ] if self.clearBtn else "",  id, js_options)

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


class DateWidget(DateTimeWidget):
    """
    DateWidget is the corresponding widget for Date filed, it renders only the date section of datetime picker.
    """

    def __init__(self, attrs=None, options=None, usel10n=None, widgets=None,  bootstrap_version=None):

        if options is None:
            options = {}

        # Set the default options to show only the datepicker object
        options['startView'] = options.get('startView', '2')
        options['minView'] = options.get('minView', '2')
        options['format'] = options.get('format', 'dd/mm/yyyy')

        if widgets is None:
            self.widgets = (DateInput(attrs=attrs),)

        super(DateWidget, self).__init__(attrs, options, usel10n, self.widgets, bootstrap_version)

    def to_local(self):
        """
        This method have to be called on every request call, because adapt the datetime format to the user.
        !!! It work only if USE_L10N is set TRUE and localize middleware is active.!!!
        otherwise get_format use the server format.
        """
        pattern = re.compile(r'(?<!\w)(' + '|'.join(dateConversiontoJavascript.keys()) + r')\b')
        self.format = get_format('DATE_INPUT_FORMATS')[0]
        if hasattr(self, 'widgets') and self.widgets[0]:
            self.widgets[0].format = self.format
        self.option = (pattern.sub(lambda x: dateConversiontoJavascript[x.group()], self.format),) + self.option[1:]
        self.language = get_language()


    def format_output(self, rendered_widgets):
        """
        Given a list of rendered widgets (as strings), it inserts an HTML
        linebreak between them.

        Returns a Unicode string representing the HTML for the whole lot.
        """
        return super(DateWidget, self).format_output(rendered_widgets).replace('glyphicon glyphicon-th', 'glyphicon glyphicon-calendar')


class TimeWidget(DateTimeWidget):
    """
    TimeWidget is the corresponding widget for Time filed, it renders only the time section of datetime picker.
    """

    def __init__(self, attrs=None, options=None, usel10n=None, widgets=None, bootstrap_version=None):

        if options is None:
            options = {}

        # Set the default options to show only the timepicker object
        options['startView'] = options.get('startView', '1')
        options['minView'] = options.get('minView', '0')
        options['maxView'] = options.get('maxView', '1')
        options['format'] = options.get('format', 'hh:ii')

        if widgets is None:
            self.widgets = (TimeInput(attrs=attrs),)

        super(TimeWidget, self).__init__(attrs, options, usel10n, self.widgets, bootstrap_version)

    def to_local(self):
        """
        This method have to be called on every request call, because adapt the datetime format to the user.
        !!! It work only if USE_L10N is set TRUE and localize middleware is active.!!!
        otherwise get_format use the server format.
        """
        pattern = re.compile(r'(?<!\w)(' + '|'.join(dateConversiontoJavascript.keys()) + r')\b')
        self.format = get_format('TIME_INPUT_FORMATS')[0]
        if hasattr(self, 'widgets') and self.widgets[0]:
            self.widgets[0].format = self.format
        self.option = (pattern.sub(lambda x: dateConversiontoJavascript[x.group()], self.format),) + self.option[1:]
        self.language = get_language()

    def value_from_datadict(self, data, files, name):
        D = super(TimeWidget, self).value_from_datadict(data, files, name)
        return D.timetz() if D != '' else D

    def format_output(self, rendered_widgets):
        """
        Given a list of rendered widgets (as strings), it inserts an HTML
        linebreak between them.

        Returns a Unicode string representing the HTML for the whole lot.
        """
        return super(TimeWidget, self).format_output(rendered_widgets).replace('glyphicon glyphicon-th', 'glyphicon glyphicon-time')

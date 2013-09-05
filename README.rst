django-datetime-widget
======================

``django-datetime-widget`` is clean and easy to configure widget for DateTimeField. It based on the famous javascript library  `bootstrap-datetimepicker
<https://github.com/smalot/bootstrap-datetimepicker>`_.

``django-datetime-widget`` is perfect when you use an DateTimeField on your model where is necessary to have a specific date time format with a clean input, now it support django localization and datetime format is adapting to user request.

Requirements
------------
* `Bootstrap  <http://twitter.github.com/bootstrap/>`_ 2.0.4+ (3.0 not yet!)
* `jQuery <http://jquery.com/>`_ 1.7.1+

Screenshots
===========

* Decade year view

.. image:: https://raw.github.com/smalot/bootstrap-datetimepicker/master/screenshot/standard_decade.png

This view allows to select the day in the selected month.

* Year view

.. image:: https://raw.github.com/smalot/bootstrap-datetimepicker/master/screenshot/standard_year.png

This view allows to select the month in the selected year.

* Month view

.. image:: https://raw.github.com/smalot/bootstrap-datetimepicker/master/screenshot/standard_month.png

This view allows to select the year in a range of 10 years.

* Day view

.. image:: https://raw.github.com/smalot/bootstrap-datetimepicker/master/screenshot/standard_day.png

This view allows to select the hour in the selected day.

* Hour view

.. image:: https://raw.github.com/smalot/bootstrap-datetimepicker/master/screenshot/standard_hour.png

This view allows to select the preset of minutes in the selected hour.
The range of 5 minutes (by default) has been selected to restrict buttons quantity to an acceptable value, but it can be overrided by the <code>minuteStep</code> property.

* Day view - meridian

.. image:: https://raw.github.com/smalot/bootstrap-datetimepicker/master/screenshot/standard_day_meridian.png

Meridian is supported in both the day and hour views.
To use it, just enable the <code>showMeridian</code> property.

* Hour view - meridian

.. image:: https://raw.github.com/smalot/bootstrap-datetimepicker/master/screenshot/standard_hour_meridian.png


Installation
------------

#. Install django-datetime-widget using pip. For example::

    pip install django-datetime-widget

#. Add  ``datetimewidget`` to your INSTALLED_APPS.

If you want to use localization:

#. Set USE_L10N = True, USE_TZ = True  and USE_I18N = True in settings.py

#. Add 'django.middleware.locale.LocaleMiddleware' to MIDDLEWARE_CLASSES in settings.py

#. When you create the widget add usel10n = True like attribute : DateTimeWidget(usel10n=True)

Basic Configuration
-------------------
#. Create your model-form and set  DateTimeWidget widget to your DateTimeField  ::

    from datetimewidget.widgets import DateTimeWidget

    class yourForm(forms.ModelForm):
        class Meta:
            model = yourModel
            widgets = {
                #Use localization
                'datetime': DateTimeWidget(attrs={'id':"yourdatetimeid"}, usel10n = True)
            }

#. Download `twitter bootstrap <http://twitter.github.com/bootstrap/>`_  to your static file folder.

#. Add in your form template links to jquery, bootstrap and form.media::

    <head>
    ....
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
        <link href="{{ STATIC_URL }}css/bootstrap.css" rel="stylesheet" type="text/css"/>
        <script src="{{ STATIC_URL }}js/bootstrap.js"></script>
        {{ form.media }}

    ....
    </head>
    <body>
        <form  action="" method="POST">
        {% csrf_token %}
        {{ form.as_table }}
        <input id="submit" type="submit" value="Submit">
        </form>
    </body>


#. Optional: you can add option dictionary to DatetimeWidget to customize your input, for example to have date time with meridian::


        dateTimeOptions = {
        'format': 'dd/mm/yyyy HH:ii P',
        'autoclose': 'true',
        'showMeridian' : 'true'
        }
        widgets = {
            #NOT Use localization and set a default format
            'datetime': DateTimeWidget(options = dateTimeOptions)
            }

!!! If you add 'format' into options and in the same time set usel10n as True the first one is ignored. !!!

Options
=======

* format

String.  Default: 'dd/mm/yyyy hh:ii'

The date format, combination of  P, hh, HH , ii, ss, dd, yy, yyyy.

 * P : meridian in upper case ('AM' or 'PM') - according to locale file
 * ss : seconds, 2 digits with leading zeros
 * ii : minutes, 2 digits with leading zeros
 * hh : hour, 2 digits with leading zeros - 24-hour format
 * HH : hour, 2 digits with leading zeros - 12-hour format
 * dd : day of the month, 2 digits with leading zeros
 * yy : two digit representation of a year
 * yyyy : full numeric representation of a year, 4 digits

* weekStart

String.  Default: '0'

Day of the week start. '0' (Sunday) to '6' (Saturday)

* startDate

Date.  Default: Beginning of time

The earliest date that may be selected; all earlier dates will be disabled.

* endDate

Date.  Default: End of time

The latest date that may be selected; all later dates will be disabled.

* daysOfWeekDisabled

String.  Default:  '[]'

Days of the week that should be disabled. Values are 0 (Sunday) to 6 (Saturday). Multiple values should be comma-separated. Example: disable weekends:  '[0,6]'.

* autoclose

String.  Default: 'true'

Whether or not to close the datetimepicker immediately when a date is selected.

* startView

String.  Default: '2'

The view that the datetimepicker should show when it is opened.
Accepts values of :
 * '0'  for the hour view
 * '1'  for the day view
 * '2'  for month view (the default)
 * '3'  for the 12-month overview
 * '4'  for the 10-year overview. Useful for date-of-birth datetimepickers.

* minView

String. Default: '0'

The lowest view that the datetimepicker should show.

* maxView

String. Default: '4'

The highest view that the datetimepicker should show.

* todayBtn

String.  Default: 'false'

If true , displays a "Today" button at the bottom of the datetimepicker to select the current date.  If true, the "Today" button will only move the current date into view.

* todayHighlight

String.  Default: 'false'

If true, highlights the current date.

* minuteStep

String.  Default: '5'

The increment used to build the hour view. A button is created for each <code>minuteStep</code> minutes.

* pickerPosition

String. Default: 'bottom-right' (other supported value : 'bottom-left')

This option allows to place the picker just under the input field for the component implementation instead of the default position which is at the bottom right of the button.

* showMeridian

String. Default: 'false'

This option will enable meridian views for day and hour views.

* clearBtn

Boolean.  Default: false

If true, displays a "Clear" button at the bottom of the datepicker to clear the input value. If "autoclose" is also set to true, this button will also close the datepicker.

CHANGELOG
---------
* Add Clear button
* Fix TypeError bug
* Support localization
* Update static file with last commit of bootstrap-datetime-picker
* update js lib, native localization, thanks to @quantum13
* autoclose is true by default

Contribute
----------

#. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug. There is a `Contributor Friendly`_ tag for issues that should be ideal for people who are not very familiar with the codebase yet.
  #. If you feel uncomfortable or uncertain about an issue or your changes, feel free to email @asagli and he will happily help you via email, Skype, remote pairing or whatever you are comfortable with.
#. Fork `the repository`_ on GitHub to start making your changes to the **master** branch (or branch off of it).
#. Please, shows that the bug was fixed or that the feature works as expected.
#. Send a pull request and bug the maintainer until it gets merged and published. :)

.. _`the repository`: https://github.com/asaglimbeni/django-datetime-widget
.. _Contributor Friendly: https://github.com/asaglimbeni/django-datetime-widget/issues?direction=desc&labels=Contributor+Friendly&page=1&sort=updated&state=open


TODO
----
#. widget for TimeField
#. widget for DateField
#. widget for DateTime range.


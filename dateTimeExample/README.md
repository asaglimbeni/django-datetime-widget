#Running the example application

Here we assume that you already have either [virtualenv](https://github.com/pypa/virtualenv) or [virtualenvwrapper](https://bitbucket.org/dhellmann/virtualenvwrapper/src/master/docs/source/index.rst) installed on your machine.

Instructions for `virtualenv`

    $ git clone https://github.com/siolag161/django-datetime-widget.git dj-datetime-widget && cd dj-datetime-widget
    $ cd dateTimeExample
    $ virtualenv dj-dtw-env && . dj-dtw-env/bin/activate
    $ pip install -r requirements.txt
    $ python manage.py syncdb
    $ python manage.py runserver

Instructions for `virtualenvwrapper`

    $ git clone https://github.com/siolag161/django-datetime-widget.git dj-datetime-widget && cd dj-datetime-widget
    $ cd dateTimeExample
    $ mkvirtualenv dj-dtw-env 
    $ pip install -r requirements.txt
    $ python manage.py syncdb
    $ python manage.py runserver 

Now you can use your favorite browser to open http://127.0.0.1:8000

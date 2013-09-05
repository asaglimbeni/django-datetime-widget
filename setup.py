__author__ = 'Alfredo Saglimbeni'

from distutils.core import setup
from setuptools import setup, find_packages

setup(name = "django-datetime-widget",
    version = "0.6",
    description = "Django-datetime-widget is a simple and clean widget for DateTimeField. It's based on bootstrap-datepicker by Stefan Petre",
    long_description=open('README.rst').read(),
    author = "Alfredo Saglimbeni",
    author_email = "alfredo.saglimbeni@gmail.com",
    url = "",
    packages = find_packages(),
    include_package_data=True,
    install_requires = ['django','pytz'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    zip_safe=False,
)
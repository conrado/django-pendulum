This application will allow users of Django-powered websites keep track of the
time they spend on different projects.  It's a work in process.

Features
========

* Configurable: Pendulum can be configured to operate on several Django-powered
  sites.  The period lengths can be configured as monthly or as a fixed-length
  period.
* Projects: You can have an unlimited number of projects to be able to
  categorize hours spent working on certain tasks.  Each project can be
  activated/deactivated as necessary via the Django admin.
* Activities: Activities allow you to further categorize work done on
  particular tasks for each project.

Requirements
============

``django-pendulum`` requires a modern version of the Django framework.  By
modern I simply mean a version with the ``newforms-admin`` functionality.  If
you're running on Django 1.0 or later, you're good.

``django-pendulum`` also relies upon the ``django.contrib.admin``,
``django.contrib.auth``, ``django.contrib.contenttypes``, and
``django.contrib.sites`` frameworks.

Installation
============

Download ``django-pendulum`` using *one* of the following methods:

pip
---

Install ``django-pendulum`` using ``pip``::

    pip install -U django-pendulum

easy_install
------------

You can download the package from the `CheeseShop
<http://pypi.python.org/pypi/django-pendulum/>`_ or use::

    easy_install django-pendulum

to download and install ``django-pendulum``.

Package Download
----------------

Download the latest ``.tar.gz`` file from the downloads section and extract it
somewhere you'll remember.  Use ``python setup.py install`` to install it.

Checkout from Version Control
-----------------------------

Clone ``django-pendulum`` using one of the official repositories::

    hg clone http://bitbucket.org/codekoala/django-pendulum
    git clone http://github.com/codekoala/django-pendulum.git
    hg clone http://django-pendulum.googlecode.com/hg django-pendulum

Verifying Installation
======================

The easiest way to ensure that you have successfully installed Pendulum is to
execute a command such as::

    python -c "import pendulum; print pendulum.get_version()"

If that displays the version of Pendulum that you tried to install, you're good
to roll.  If you see something other than that, you probably need to check your
``PYTHONPATH`` environment variable.

Configuration
=============

First of all, you must add this project to your list of ``INSTALLED_APPS`` in
``settings.py``::

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        ...
        'pendulum',
        ...
    )

Run ``manage.py syncdb``.  This creates a few tables in your database that are
necessary for operation.

Next, you should add an entry to your main ``urls.py`` file.  For example::

    from django.conf.urls.defaults import *

    from django.contrib import admin
    admin.autodiscover()

    urlpatterns = patterns('',
        (r'^admin/(.*)', admin.site.root),
        (r'^pendulum/', include('pendulum.urls')),
    )

The next thing you will want to do is configure Pendulum for the active Django
sites.  Do this by going into the Django admin and clicking the "add" link next
to Pendulum Configurations.

The first step in the configuration is to choose which site this particular
configuration will apply to.  The decision is easy if you only have one site :)

Next, you must choose what kind of "accounting period" you wish to use.  If you
want month-long periods, ensure the "Is monthly" check box is selected.  Then
enter the day of the month that the periods begin.  Periods that begin on the
first of the month will always range from midnight on the first of each month
to 11:59:59 PM on the last day of each month.  Periods that begin on the 16th
of the month will range from midnight on the 16th of each month to 11:59:59 PM
on the 15th of the following month.  Be wise about choosing start days such as
the 31st of the month--it's not a wise choice no matter what situation you're
in.

Alternatively, you may choose fixed-length accounting periods.  The
installation date does not necessarily have to be the actual installation date.
This field is used as a reference point for creating periods.  For example, if
you have 2-week long accounting periods that begin on Sundays and end two
Saturdays later, you would select _any_ Sunday from any month from any year.
Then you would enter 14 for the period length.  Periods will automatically be
constructed that will begin at midnight each Sunday and end at 11:59:59 PM two
Saturdays in the future.

If you fail to configure Pendulum for a given site, you will likely receive
HTTP 500 errors if you try to access Pendulum via the front-end.

Add Projects
------------

Next, you should add at least one project to Pendulum.  This can easily be
accomplished via the Django admin.  The same goes for activities, but these are
not required.

Permissions
-----------

Finally, be sure set people up with the appropriate permissions using Django's
Auth framework.  The front end side of Pendulum respects these permissions.
That means that if a user doesn't have the permission to clock in, the will be
presented with a login screen (even if they're logged in already) when they try
to clock in on the front end site.  The same goes for other operations such as
pausing/unpausing entries, updating entries, deleting entries, etc.

An easy way to assign the same Pendulum permissions to several users is to
create a Group using the Auth framework.  There is a custom command for
creating a group with all of the permissions necessary for the front end,
including the ability to:

* add entries
* update entries
* delete entries
* clock in
* clock out
* pause/unpause entries

To use this command, simply run ``python manage.py create_pendulum_group``.
You may run ``python manage.py help create_pendulum_group`` to learn about
options for this command.

The Date Field
==============

I've been hesitant to do anything to make the date/time fields more
user-friendly when adding or updating entries.  I don't want to tie anyone down
to my particular way of doing things.  I personally prefer jQuery for this sort
of thing, but I do realize that jQuery disgusts many other people out there.
Therefore, the first versions of the application didn't come with anything to
make those fields easier to use and understand.

However, that seems to be the most common complaint amongst those who have
played with the application--the lack of user-friendly date pickers.  As such,
I have added some jQuery-based utilities to make choosing a date easier and
more intuitive.

By default, the application will expect to find the appropriate files in a
directory called ``pendulum`` within your media directory.  All you should need
to do is copy or symlink the ``media`` folder from the Pendulum application
directory.  If you copy the ``media`` folder, rename it to ``pendulum``.  If
you create a symlink to Pendulum's ``media`` folder, make sure the symlink is
called ``pendulum``.  This directory should hold all of the necessary files to
make the date picker work.

In your ``add_update_entry.html`` template (if you override the default ones),
make sure you have a code block such as::

    {% block extra-head %}
    {{ form.media }}
    <script type="text/javascript">
    $(document).ready(function () {
        $('input.vDateField').datepicker({
                dateFormat: $.datepicker.W3C,
                showOn: 'both',
                buttonImage: '{{ MEDIA_URL }}pendulum/img/calendar.png',
                buttonImageOnly: true
            });
    });
    </script>
    {% endblock %}

This is just jQuery's way of attaching the date picker to the appropriate
fields.

Customizing The Date Picker
---------------------------

I tried to put some utilities in the application to allow you to change the
date picker that is used with ease.  There is a variable that you can define in
your ``settings.py`` file to override the default date picker:
``PENDULUM_DATE_MEDIA``.  If you simply want to change the styling CSS, for
example, you could use this variable.  The default value is::

    PENDULUM_DATE_MEDIA = {
        'js': (settings.MEDIA_URL + 'pendulum/js/jquery.js',
                settings.MEDIA_URL + 'pendulum/js/jquery.ui.js'),
        'css': {
            'all': (settings.MEDIA_URL + 'pendulum/css/jquery-ui.css',)
        }
    }

You can see that it is a dictionary with two keys: ``js`` and ``css``.  The
values of these two items conform to the concepts outlined in `Django's
documentation <http://docs.djangoproject.com/en/dev/topics/forms/media/>`_.
Changing the values within ``PENDULUM_DATE_MEDIA`` should permit you to
completely remove or replace the date picker as you desire.

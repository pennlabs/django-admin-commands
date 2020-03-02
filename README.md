# Django Admin Commands

[![CircleCI](https://circleci.com/gh/pennlabs/django-admin-commands.svg?style=shield)](https://circleci.com/gh/pennlabs/django-admin-commands)
[![Coverage Status](https://codecov.io/gh/pennlabs/django-admin-commands/branch/master/graph/badge.svg)](https://codecov.io/gh/pennlabs/django-admin-commands)
[![PyPi Package](https://img.shields.io/pypi/v/django-admin-commands.svg)](https://pypi.org/project/django-admin-commands/)

## Requirements

* Python 3.6+
* Django 2.2+

## Demo/Test

If wanting to demo/test the package it self, you can use the penn clubs app, through the admin-commands-test branch (https://github.com/pennlabs/penn-clubs/tree/admin-commands-test)

After installing the application, migrating and creating a super user you should be able to access the command interface at ``localhost/api/commands``. You might need to login as admin first.

## Installation

Install with pip `pip install django-admin-commands`

Add ``admin_commands`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'admin_commands',
    )

Add the ``admin_commands`` URLs to your ``urls.py``

.. code-block:: python

    urlpatterns = patterns('',
        ...
        path("commands/", include("admin_commands.urls", namespace="commands")),
    )

Note: The url can be whatever you prefer.

You HAVE to have `DJANGO_PROJECT_ROOT` in your settings pointing towards the
directory of your `manage.py` file.


## Settings
### ADMIN_COMMANDS_DISPLAYED_APPS

You can limit the displayed apps by setting
``ADMIN_COMMANDS_DISPLAYED_APPS``. The syntax is the same as it is in the
``INSTALLED_APPS`` setting. It defaults to showing absolutely all apps.

    # would list all commands of the example_app
    ADMIN_COMMANDS_DISPLAYED_APPS = ['example_app']

### ADMIN_COMMANDS_DISPLAYED_COMMANDS

Further you can also provide a list of commands, that should explicitly be
displayed. Defaults to all as well.


    # would on its own only show the mycommand command
    ADMIN_COMMANDS_DISPLAYED_COMMANDS = ['mycommand']


The settings don't exclude each other. So displaying any full app and just one
or two specific commands from somewhere else is no problem at all.

### ADMIN_COMMANDS_LOGFILE_PATH

For logging, you can specify a logfile path, where logfiles for each command
can be created. The logfiles will always be prefixed with
``command_interface_log-``.


    ADMIN_COMMANDS_LOGFILE_PATH = '/home/myname/tmp/logs/'

This value defaults to ``None``, which means, that no logs are created, and the output of the commands is not shown.

The log of the last run is then displayed on the command interface
under each respective command.


## Documentation

... TODO

## Changelog

See [CHANGELOG.md](https://github.com/pennlabs/django-admin-commands/blob/master/CHANGELOG.md)

## License

See [LICENSE](https://github.com/pennlabs/django-admin-commands/blob/master/LICENSE)

Originally based on django-command-interface by bitlabstudio. (https://github.com/bitlabstudio/django-command-interface)

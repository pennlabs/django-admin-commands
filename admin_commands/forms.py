"""Forms for the ``django-admin-commands`` app."""
import os
import subprocess
from collections import namedtuple

from django import forms
from django.conf import settings
from django.core.management import get_commands, load_command_class, call_command
from django.utils.translation import ugettext_lazy as _
from io import StringIO

from .exceptions import CommandError
from . import settings as app_settings

from pprint import pprint


class CommandExecutionForm(forms.Form):
    """Form, that executes a manage.py command."""

    command = forms.CharField()
    arguments = forms.CharField(
        label=_('Arguments'),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(CommandExecutionForm, self).__init__(*args, **kwargs)
        self.command_dict = get_commands()
        self.allowed_commands = []
        apps = {}
        for command_name, app_name in self.command_dict.items():
            if self.command_allowed(command_name, app_name):
                # pprint('loading ' + command_name)
                self.allowed_commands.append(command_name)
                command_class = load_command_class(app_name, command_name)
                # pprint(command_class)
                # creating an optionparser
                optparser = command_class.create_parser(
                    './manage.py', command_name)
                # pprint(optparser)
                # get the docstring from the parser
                docstring = ''
                if optparser.usage is not None:
                    docstring = optparser.usage.replace('%prog', './manage.py')
                # pprint('docstring: ' + docstring)
                # get the options
                options = []
                Option = namedtuple('Option', ['opt_string', 'help'])
                # pprint(getattr(optparser, 'option_list', []))
                for opt in getattr(optparser, 'option_list', []):
                    pprint(opt)
                    if opt.dest is not None:
                        dest = opt.dest.upper()
                    else:
                        dest = ''
                    opt_string = ','.join(opt._long_opts)
                    if dest:
                        opt_string += '={0}'.format(dest)
                    if opt._short_opts:
                        opt_string = '{0} {1}, '.format(
                            ','.join(opt._short_opts), dest) + opt_string
                    options.append(Option(opt_string, opt.help))

                Command = namedtuple('Command', ['command', 'docstring',
                                                 'options', 'log', 'help_text'])
                if command_class.__doc__ is not None:
                    # in case there's a docstring on the class, prepend it to
                    # make sure all description is included.
                    docstring = command_class.__doc__ + '\n\n' + docstring

                log = None
                if app_settings.LOGFILE_PATH is not None:
                    file_name = os.path.join(
                        app_settings.LOGFILE_PATH,
                        'command_interface_log-{0}.log'.format(command_name))
                    try:
                        with open(file_name, 'r') as f:
                            log = f.read()
                    except IOError:
                        pass

                # Get help from command
                # TODO improve this - subprocess does not seem like the best option
                # but call_command throws an exception when help is called (unknown why)
                project_root = settings.DJANGO_PROJECT_ROOT
                manage_py = os.path.join(project_root, 'manage.py')
                venv = os.environ.get('VIRTUAL_ENV', None)
                python = '/usr/bin/python'
                if venv is not None:
                    python = os.path.join(venv, 'bin/python')
                help_text = subprocess.check_output([python, manage_py, command_name, '--help'])

                command = Command(command_name, docstring, options, log, help_text)
                App = namedtuple(app_name.replace('.', '_'),
                                 ['app_name', 'commands'])
                if not app_name in apps:
                    apps[app_name] = App(app_name, [command])
                else:
                    apps[app_name].commands.append(command)
        self.apps = apps.values()

    def clean(self):
        cleaned_data = super(CommandExecutionForm, self).clean()
        command = cleaned_data.get('command')
        if command not in self.allowed_commands:
            raise forms.ValidationError(_(
                'The command you tried to execute is not among the permitted'
                ' ones.'))
        return cleaned_data

    def command_allowed(self, command_name, app_name):
        """Returns whether or not the command or app should be listed."""
        if not app_settings.DISPLAYED_APPS and \
                not app_settings.DISPLAYED_COMMANDS:  # pragma: nocover
            return True
        if command_name in app_settings.DISPLAYED_COMMANDS or \
                app_name in app_settings.DISPLAYED_APPS:
            return True
        return False

    def execute(self):
        """
        Calls the command, that was entered.
        :test_run: Only required by testrunners, so that we wait for the
          command to finish.
        """
        command = self.cleaned_data.get('command')
        arguments = self.cleaned_data.get('arguments')
        pprint("command " + command + " called")
        project_root = settings.DJANGO_PROJECT_ROOT
        manage_py = os.path.join(project_root, 'manage.py')
        venv = os.environ.get('VIRTUAL_ENV', None)
        python = '/usr/bin/python'
        if venv is not None:
            python = os.path.join(venv, 'bin/python')
        popen_args = [python, manage_py, command]
        result = StringIO()
        try:
            if arguments:
                pprint('Args: ' + arguments)
                popen_args.append(arguments)
                call_command(command, arguments, stdout=result, stderr=result)
            else:
                pprint('No args')
                call_command(command, stdout=result, stderr=result)
        # TODO: Actually make this work (does not recognize exception)
        except CommandError:
            pprint('error got')
        
        #subprocess.Popen(popen_args, stdout=result)

        pprint('Passed subprocess')

        pprint('Result:' + result.getvalue())

        pprint(app_settings.LOGFILE_PATH)

        if app_settings.LOGFILE_PATH is not None:
            file_name = os.path.join(
                app_settings.LOGFILE_PATH,
                'command_interface_log-{0}.log'.format(command))
            try:
                with open(file_name, 'w') as f:
                    pprint("writing to file")
                    f.write(result.getvalue())
            except IOError:
                raise CommandError('Could not open file for writing log.')

import argparse
from os import environ
import re

class EnvDefault(argparse.Action):
    __ALLOWED_VARNAME_REGEX = re.compile("^[a-zA-Z_][a-zA-Z0-9_]+$")

    @staticmethod
    def __auto_varname(options):
        name = ''
        options = [x for x in options if x.startswith('-')]
        if options:
            name = max(options, key=len)
            if name[0:2] == '--':
                name = name[2:]
            elif name[0] == '-':
                name = name[1:]
            name = name.replace('-', '_').upper()
        return name

    def __init__(self, envvar=None, default=None, **kwargs):
        if not envvar:
            options = kwargs.get('option_strings')
            if not isinstance(options, list):
                options = []
            envvar = self.__auto_varname(options)

        if not self.__ALLOWED_VARNAME_REGEX.match(envvar):
            raise Exception('Invalid environment variable name: ' + envvar)

        if envvar in environ:
            default = environ[envvar]
            if kwargs.get('required'):
                kwargs['required'] = False

        super(EnvDefault, self).__init__(default=default, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)

class Argument:
    def __init__(self,
                 name='',
                 abbreviation_name='',
                 full_name='',
                 value=None,
                 help_message='',
                 metavar='',
                 default='None',
                 to_save=False,
                 is_main=False,
                 command=None,
                 command_args=None,
                 choices=None,
        """
        :param name: the name of the argument, ex: alias (must be the same as full_name)
        :param abbreviation_name: the abbreviation name for the argument, ex: -a (see argsparse documentation https://docs.python.org/3/library/argparse.html#name-or-flags)
        :param full_name: the full name of the argument, ex: --alias (must be the same as name) (see argsparse documentation https://docs.python.org/3/library/argparse.html#name-or-flags)
        :param value: the value of the argument provided posteriorly by the user.
        :param help_message: the help message for the argument (see argsparse documentation https://docs.python.org/3/library/argparse.html#help)
        :param metavar: the metavar for the argument (see argsparse documentation https://docs.python.org/3/library/argparse.html#metavar)
        :param default: the default value for the argument
        :param to_save: a boolean defining if this argument should be saved in the yaml file.
        :param is_main: a boolean defining if this argument is a main argument. There must be 1 if to use on RepeatableSettings class
        :param command: the method that this argument should call when it's present on the arguments parsed and provided by the user.
        :param command_args: all the arguments the previous method needs to have. If more than one argument, please wrap them in (), ex: (arg1, arg2)
        :param choices: a list of choices required by the argument (see argsparse documentation
        https://docs.python.org/3/library/argparse.html#choices)
        """
        self.name = name
        self.abbreviation_name = abbreviation_name
        self.full_name = full_name
        self.value = value
        self.help_message = help_message
        self.metavar = metavar
        self.default = default
        self.to_save = to_save
        self.is_main = is_main
        self.command = command
        self.command_args = command_args
        self.choices = choices

    @staticmethod
    def set_argument(argument):
        return Argument(
            name=argument.name,
            abbreviation_name=argument.abbreviation_name,
            full_name=argument.full_name,
            value=argument.value,
            help_message=argument.help_message,
            metavar=argument.metavar,
            default=argument.default,
            to_save=argument.to_save,
            is_main=argument.is_main,
            command=argument.command,
            command_args=argument.command_args,
            choices=argument.choices,

    def set_value(self, value):
        self.value = value

    def set_command(self, command):
        self.command = command

    def set_command_args(self, command_args):
        """
        If more than one argument, please wrap them in (), ex: (arg1, arg2)
        :param command_args: all the arguments required by the method/command
        :return: command the arguments defined
        """
        self.command_args = command_args

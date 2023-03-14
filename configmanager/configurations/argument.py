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
                 command_args=None):
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
            command_args=argument.command_args)

    def set_value(self, value):
        self.value = value

    def set_command(self, command):
        self.command = command

    def set_command_args(self, command_args):
        self.command_args = command_args



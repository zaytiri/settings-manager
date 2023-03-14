import argparse

from configmanager.configurations.argument import Argument
from configmanager.configurations.arguments import Arguments


class Specific(Arguments):
    are_configs_saved = False

    def __init__(self):
        self.alias = Argument(name='alias',
                              abbreviation_name='-a',
                              full_name='--alias',
                              help_message='chosen UNIQUE alias for the file. when updating any configurations this flag needs to be used. this only '
                                           'works if the file path already exists in the configurations.',
                              metavar="",
                              to_save=True,
                              is_main=True)

        self.executable_path = Argument(name='executable_path',
                                        abbreviation_name='-e',
                                        full_name='--executable-path',
                                        help_message='absolute path of file to schedule.',
                                        metavar="",
                                        to_save=True)

        self.days = Argument(name='days',
                             abbreviation_name='-d',
                             full_name='--days',
                             help_message='days of the week for when the file will start. multiple values can be set. available set of values: '
                                          '\'monday\', \'tuesday\', \'wednesday\', '
                                          '\'thursday\', \'friday\', \'saturday\' and \'sunday\'.',
                             metavar="",
                             to_save=True,
                             default=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'everyday',
                                      'weekdays', 'weekends'])

        self.time = Argument(name='time',
                             abbreviation_name='-t',
                             full_name='--time',
                             help_message='input a specific time to start the file. example: \'08:15\'. default value is: \'at startup\'. If is \'at '
                                          'startup\' '
                                          'then the file will be scheduled to open at startup.',
                             metavar="",
                             to_save=True,
                             default='at startup')

        self.job = Argument(name='job',
                            abbreviation_name='-j',
                            full_name='--job',
                            help_message='specifies the job the scheduler is going to do. example: -j',
                            metavar="",
                            to_save=True,
                            default=['open_program'])

    def set_are_configs_saved(self, are_configs_saved):
        self.are_configs_saved = are_configs_saved

    def add_arguments(self, argument_parser):
        argument_parser.add_argument(self.executable_path.abbreviation_name, self.executable_path.full_name,
                                     required=not self.are_configs_saved,
                                     help=self.executable_path.help_message,
                                     metavar=self.executable_path.metavar,
                                     default=argparse.SUPPRESS)

        argument_parser.add_argument(self.alias.abbreviation_name, self.alias.full_name,
                                     required=not self.are_configs_saved,
                                     help=self.alias.help_message,
                                     metavar=self.alias.metavar,
                                     default=argparse.SUPPRESS)

        argument_parser.add_argument(self.days.abbreviation_name, self.days.full_name,
                                     required=not self.are_configs_saved,
                                     nargs='*',
                                     choices=self.days.default,
                                     help=self.days.help_message,
                                     metavar=self.days.metavar,
                                     default=argparse.SUPPRESS)

        argument_parser.add_argument(self.job.abbreviation_name, self.job.full_name,
                                     required=not self.are_configs_saved,
                                     choices=self.job.default,
                                     help=self.job.help_message,
                                     metavar=self.job.metavar,
                                     default=argparse.SUPPRESS)

        argument_parser.add_argument(self.time.abbreviation_name, self.time.full_name,
                                     type=str,
                                     help=self.time.help_message,
                                     metavar=self.time.metavar,
                                     default=self.time.default)

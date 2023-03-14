import os

from configmanager.settings.generic_arguments import Generic
from configmanager.settings.specific_arguments import Specific
from configmanager.services.directory import Directory
from configmanager.configurations.configurations import Configurations
from configmanager.utils.log import throw
from configmanager.utils.progsettings import get_version
import argparse


class Manager:
    is_to_configure = False

    def __init__(self):
        self.args = argparse.ArgumentParser()
        self.args.add_argument('--version', action='version', version='%(prog)s ' + str(get_version()))

    def configure_arguments(self):
        # manage specific configurations
        specific_arguments = Specific()
        specific_config = Configurations(path=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'local.yaml'),
                                         program_arguments=specific_arguments,
                                         is_repeatable=True)
        specific_arguments.are_configs_saved = specific_config.is_configured()
        specific_arguments.add_arguments(self.args)

        # manage generic configurations
        generic_arguments = Generic()
        generic_config = Configurations(path=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'global.yaml'),
                                        program_arguments=generic_arguments)
        generic_arguments.add_arguments(self.args)

        # parse configurations from user input
        user_arguments = self.args.parse_args()
        specific_config.set_user_arguments(user_arguments)
        generic_config.set_user_arguments(user_arguments)

        # set command arguments
        generic_arguments.list_all_configs.set_command_args(specific_config.file.path)
        generic_arguments.delete.set_command_args((specific_config.user_arguments, specific_config.file.path))

        # define and check rules for specific arguments
        self.__process_specific_arguments(specific_arguments, specific_config)

        specific_program_args = specific_config.process()
        generic_program_args = generic_config.process()

        self.is_to_configure = specific_config.is_to_configure
        return [specific_program_args, generic_program_args]

    def __process_specific_arguments(self, specific_arguments, specific_config):
        self.__check_any_errors(specific_arguments)

        if specific_arguments.days.name in specific_config.user_arguments:
            every_day_of_week = specific_arguments.days.default
            if specific_config.user_arguments.days[0] == 'everyday':
                specific_config.user_arguments.days = self.get_specific_days('everyday', every_day_of_week)
            elif specific_config.user_arguments.days[0] == 'weekdays':
                specific_config.user_arguments.days = self.get_specific_days('weekdays', every_day_of_week)
            elif specific_config.user_arguments.days[0] == 'weekends':
                specific_config.user_arguments.days = self.get_specific_days('weekends', every_day_of_week)

    def __check_any_errors(self, specific_arguments):
        try:
            if not self.__given_argument_path_exists(specific_arguments.executable_path):
                throw(specific_arguments.executable_path + '\' path does not exist.')
        except (AttributeError, TypeError):
            pass

    @staticmethod
    def get_specific_days(days, full_list_of_days):
        if days == 'weekdays':
            full_list_of_days.pop(full_list_of_days.index('saturday'))
            full_list_of_days.pop(full_list_of_days.index('sunday'))
        elif days == 'weekends':
            full_list_of_days.pop(full_list_of_days.index('monday'))
            full_list_of_days.pop(full_list_of_days.index('tuesday'))
            full_list_of_days.pop(full_list_of_days.index('wednesday'))
            full_list_of_days.pop(full_list_of_days.index('thursday'))
            full_list_of_days.pop(full_list_of_days.index('friday'))

        full_list_of_days.pop(full_list_of_days.index('everyday'))
        full_list_of_days.pop(full_list_of_days.index('weekdays'))
        full_list_of_days.pop(full_list_of_days.index('weekends'))

        return full_list_of_days

    @staticmethod
    def __given_argument_path_exists(path):
        argument_path = Directory(path)
        return argument_path.exists()

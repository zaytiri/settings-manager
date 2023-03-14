from configmanager.configurations.argument import Argument
from configmanager.services.directory import Directory
from configmanager.configurations.file import File
from configmanager.configurations.yaml import read_yaml, write_yaml
from configmanager.utils.log import show
from configmanager.configurations.reflection import get_class_variables


class Configurations:
    __main_arg = {'name': '', 'value': ''}
    __values_from_file = {}
    user_arguments = None
    program_arguments = None
    file = None
    is_to_configure = False

    def __init__(self, path, is_repeatable=False, program_arguments=None, user_arguments=None, show_saved_configurations=False):
        self.file = File(path)
        self.is_repeatable = is_repeatable
        self.program_arguments = program_arguments
        self.user_arguments = user_arguments
        self.show_saved_configurations = show_saved_configurations

    def set_user_arguments(self, user_arguments):
        self.user_arguments = user_arguments

    def set_program_arguments(self, program_arguments):
        self.program_arguments = program_arguments

    def set_is_repeatable(self, is_repeatable):
        self.is_repeatable = is_repeatable

    def process(self):
        self.__do_commands()

        self.__process_main_arg()

        if self.is_configured():
            self.__get_configs_from_file()

        self.__set_configurations()

        if self.to_save_configs():
            self.__save_configurations()

        return self.program_arguments

    def to_save_configs(self):
        if self.__main_arg['name'] in self.user_arguments:
            self.is_to_configure = True
        return self.is_to_configure

    def __set_configurations(self):
        try:
            if self.__main_arg['name'] in self.user_arguments:
                self.__populate_configurations(self.__values_from_file[self.__main_arg['value']])
                return
        except(AttributeError, KeyError):
            pass

        if not self.is_repeatable:
            self.__populate_configurations(self.__values_from_file)
            return

        for val in self.__values_from_file:
            self.__populate_configurations(self.__values_from_file[val])

    def __do_commands(self):
        non_saved_arguments = self.program_arguments.to_list(is_saved=[False])
        for arg in non_saved_arguments:
            if arg.name in self.user_arguments:
                if arg.command_args is not None:
                    if isinstance(arg.command_args, tuple):
                        arg.command(*arg.command_args)
                    else:
                        arg.command(arg.command_args)
                else:
                    arg.command()

    def __get_configs_from_file(self):
        self.__values_from_file = read_yaml(self.file.path)

    def __process_main_arg(self):
        try:
            for arg in self.program_arguments.to_list():
                if arg.is_main:
                    self.__main_arg['name'] = arg.name
                    break

            if self.__main_arg['name'] in self.user_arguments:
                self.__main_arg['value'] = getattr(self.user_arguments, self.__main_arg['name'])
        except (AttributeError, KeyError):
            pass

    def is_configured(self):
        directory = Directory(self.file.path)
        if not directory.exists():
            return False

        if self.file.is_empty():
            return False
        return True

    def __populate_configurations(self, values_to_populate):
        arguments = self.program_arguments.to_list()

        is_file_configured = self.is_configured()
        for configuration in arguments:
            configuration.populate(self.user_arguments, values_to_populate, is_file_configured)

            if configuration.is_main:
                self.__main_arg['value'] = configuration.value

        self.program_arguments.from_list(arguments)

    def __save_configurations(self):
        arguments = self.program_arguments.to_list([True])
        values_to_save = {}
        for arg in arguments:
            values_to_save[arg.name] = arg.value

        list_of_configs = {}

        if self.is_configured():
            list_of_configs = read_yaml(self.file.path)

        if not self.is_repeatable:
            list_of_configs = values_to_save
        else:
            list_of_configs[self.__main_arg['value']] = values_to_save

        write_yaml(self.file.path, list_of_configs)

        if self.show_saved_configurations:
            self.__show_saved_configurations()

    def __show_saved_configurations(self):
        class_variables = get_class_variables(self.program_arguments)

        show('Saved configurations:')
        message = ''
        for var in class_variables:
            if not isinstance(var[1], Argument):
                continue

            arg = Argument().set_argument(var[1])

            if arg.to_save in [True]:
                message += '\n\t\t\t' + arg.name + ': ' + str(arg.value)

        show(message)
        show('\nConfiguration file path: ' + self.file.path)

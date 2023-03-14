from configmanager.configurations.argument import Argument
from configmanager.services.directory import Directory
from configmanager.configurations.file import File
from configmanager.configurations.yaml import read_yaml, write_yaml
from configmanager.utils.log import show
from configmanager.configurations.reflection import get_class_variables


class Settings:
    program_arguments = None
    settings_from_file = {}
    values_to_save = {}
    file = None
    save_condition = False
    user_arguments = None

    def __init__(self, path, program_arguments=None, show_saved_configurations=False):
        self.file = File(path)
        self.program_arguments = program_arguments
        self.show_saved_configurations = show_saved_configurations

    def process(self):
        self.__do_commands()

        if self.is_configured():
            self.__get_configs_from_file()

        self.__set_configurations()

        if self.save_condition:
            self.__save_configurations()

        return self.program_arguments

    def __set_configurations(self):
        raise NotImplementedError("This method needs to be implemented.")

    def __save_configurations(self):
        raise NotImplementedError("This method needs to be implemented.")

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
        self.settings_from_file = read_yaml(self.file.path)

    def is_configured(self):
        directory = Directory(self.file.path)
        if not directory.exists():
            return False

        if self.file.is_empty():
            return False
        return True

    def __populate_configurations(self, values_from_file):
        arguments = self.program_arguments.to_list()

        for configuration in arguments:
            self.__populate(self.user_arguments, values_from_file)

            if configuration.save_condition:
                self.values_to_save[configuration.name] = configuration.value

        self.program_arguments.from_list(arguments)

    def __populate(self, config, values_from_file):
        if config.name in self.user_arguments:
            argument_value = getattr(self.user_arguments, config.name)
            config.set_value(argument_value)

        if self.is_configured():
            argument_value = values_from_file[config.name]
        else:
            argument_value = config.default

        config.set_value(argument_value)

    def __show_saved_configurations(self):
        class_variables = get_class_variables(self.program_arguments)

        show('Saved configurations:')
        message = ''
        for var in class_variables:
            if not isinstance(var[1], Argument):
                continue

            arg = Argument().set_argument(var[1])

            if arg.save_condition in [True]:
                message += '\n\t\t\t' + arg.name + ': ' + str(arg.value)

        show(message)
        show('\nConfiguration file path: ' + self.file.path)

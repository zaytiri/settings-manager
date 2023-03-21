import os.path

from margument.options import Options
from margument.file import File
from margument.yaml import read_yaml
from margument.log import show


class Settings:

    def __init__(self, path, program_arguments=None, options=Options()):
        self.file = File(path)
        self.program_arguments = program_arguments
        self.settings_from_file = {}
        self.values_to_save = {}
        self.user_arguments = None
        self.configs = {}
        self.options = options

        if self.exists():
            self.load()

    def set(self):
        raise NotImplementedError("This method needs to be implemented.")

    def save(self):
        raise NotImplementedError("This method needs to be implemented.")

    def do_commands(self):
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

    def load(self):
        self.settings_from_file = read_yaml(self.file.path)

    def exists(self):
        if not os.path.exists(self.file.path):
            return False

        if self.file.is_empty():
            return False
        return True

    def set_arguments_values(self, values_from_file):
        program_arguments = self.program_arguments.__class__()
        arguments = program_arguments.to_list()

        for configuration in arguments:
            self.__set_settings_value(configuration, values_from_file)

            if configuration.to_save:
                self.values_to_save[configuration.name] = configuration.value

        program_arguments.from_list(arguments)

        return program_arguments

    def __set_settings_value(self, config, values_from_file):
        if config.name in values_from_file:
            argument_value = values_from_file[config.name]
        else:
            argument_value = config.default

        config.set_value(argument_value)

    def save_when_different(self):
        if not self.options.save_different:
            return self.options.save_different

        if self.settings_from_file == self.values_to_save:
            return False
        return True

    def show(self, arguments):
        message = 'Saved configurations:'
        for name, value in arguments.items():
            message += '\n\t\t\t' + name + ': ' + str(value)

        show(message + '\n\n\t\tConfiguration file path: ' + self.file.path)

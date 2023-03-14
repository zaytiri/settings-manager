from configmanager.configurations.settings import Settings
from configmanager.configurations.yaml import read_yaml, write_yaml


class RepeatableSettings(Settings):
    __main_arg = {'name': '', 'value': ''}

    def __init__(self, path, program_arguments=None, show_saved_configurations=False):
        super().__init__(path, program_arguments, show_saved_configurations)

    def __process_main_arg(self):
        for arg in self.program_arguments.to_list():
            if arg.is_main:
                self.__main_arg['name'] = arg.name
                break

        if self.__main_arg['name'] in self.user_arguments:
            self.__main_arg['value'] = getattr(self.user_arguments, self.__main_arg['name'])

    def __set_configurations(self):
        self.__process_main_arg()

        if self.__main_arg['name'] in self.user_arguments:
            self.__populate_configurations(self.settings_from_file[self.__main_arg['value']])
            return

        for saved_setting in self.settings_from_file:
            self.__populate_configurations(self.settings_from_file[saved_setting])

    def __save_configurations(self):
        arguments = self.program_arguments.to_list([True])
        values_to_save = {}
        for arg in arguments:
            values_to_save[arg.name] = arg.value

        self.settings_from_file[self.__main_arg['value']] = values_to_save

        write_yaml(self.file.path, self.settings_from_file)

        if self.show_saved_configurations:
            self.__show_saved_configurations()

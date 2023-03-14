from configmanager.configurations.settings import Settings
from configmanager.configurations.yaml import read_yaml, write_yaml


class NonRepeatableSettings(Settings):

    def __init__(self, path, program_arguments=None, show_saved_configurations=False):
        super().__init__(path, program_arguments, show_saved_configurations)

    def __set_configurations(self):
        self.__populate_configurations(self.settings_from_file)

    def __save_configurations(self):
        arguments = self.program_arguments.to_list([True])
        values_to_save = {}
        for arg in arguments:
            values_to_save[arg.name] = arg.value

        write_yaml(self.file.path, values_to_save)

        if self.show_saved_configurations:
            self.__show_saved_configurations()

from configmanager.configurations.options import Options
from configmanager.configurations.settings import Settings
from configmanager.configurations.yaml import write_yaml


class NonRepeatableSettings(Settings):

    def __init__(self, path, program_arguments=None, options=Options()):
        super().__init__(path, program_arguments, options)

    def set(self):
        arguments = self.program_arguments.to_list()
        for arg in arguments:
            if arg.name in self.user_arguments:
                self.configs[arg.name] = getattr(self.user_arguments, arg.name)
                continue

            if arg.name in self.settings_from_file:
                self.configs[arg.name] = self.settings_from_file[arg.name]
                continue

            self.configs[arg.name] = arg.default

        self.configs = self.set_arguments_values(self.configs)

    def save(self):
        if self.save_when_different() or self.options.custom_save:
            write_yaml(self.file.path, self.values_to_save)

            if self.options.show_saved:
                self.show(self.values_to_save)

        return self.configs

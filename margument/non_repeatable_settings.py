from margument.options import Options
from margument.settings import Settings
from margument.yaml import write_yaml


class NonRepeatableSettings(Settings):

    def __init__(self, path, program_arguments=None, options=Options()):
        super().__init__(path, program_arguments, options)

    def set(self):
        self.configs = self.set_arguments_values(self.settings_from_file)

    def set_settings_value(self, config, values_from_file):
        if config.name in self.user_arguments:
            value = getattr(self.user_arguments, config.name)
        elif config.name in self.settings_from_file:
            value = self.settings_from_file[config.name]
        else:
            value = config.default

        config.set_value(value)

        if config.to_save:
            self.values_to_save[config.name] = config.value

    def save(self):
        if self.save_when_different() or self.options.custom_save:
            write_yaml(self.file.path, self.values_to_save)

            if self.options.show_saved:
                self.show(self.values_to_save)

        return self.configs

from margument.log import throw
from margument.options import Options
from margument.reflection import convert_to_dict
from margument.settings import Settings
from margument.yaml import write_yaml


class RepeatableSettings(Settings):
    __main_arg = {'name': '', 'value': ''}

    def __init__(self, path, program_arguments=None, options=Options()):
        super().__init__(path, program_arguments, options)

    def __process_main_arg(self):
        main_arg_exists = False
        for arg in self.program_arguments.to_list():
            if arg.is_main:
                main_arg_exists = True
                self.__main_arg['name'] = arg.name
                break

        if not main_arg_exists:
            throw("No main argument defined.")

        if self.__main_arg['name'] in self.user_arguments:
            self.__main_arg['value'] = getattr(self.user_arguments, self.__main_arg['name'])

    def set(self):
        self.__process_main_arg()

        user_arguments_dict = convert_to_dict(self.user_arguments)

        if not self.exists():
            try:
                self.configs[self.__main_arg['value']] = self.set_arguments_values(user_arguments_dict)
            except KeyError:
                pass
            return

        for saved_setting in self.settings_from_file:
            self.configs[saved_setting] = self.set_arguments_values(self.settings_from_file[saved_setting])

        if self.__main_arg['name'] not in self.user_arguments:
            return

        if self.__main_arg['value'] not in self.configs:
            self.configs[self.__main_arg['value']] = self.set_arguments_values(user_arguments_dict)

    def set_settings_value(self, config, values_from_file):
        is_main = False
        if self.__main_arg['value'] != '':
            is_main = values_from_file[self.__main_arg['name']] == self.__main_arg['value']

        if config.name in self.user_arguments and is_main:
            value = getattr(self.user_arguments, config.name)
        else:
            if config.name in values_from_file:
                value = values_from_file[config.name]
            else:
                value = config.default

        config.set_value(value)
        if config.to_save and is_main:
            self.values_to_save[config.name] = config.value

    def save_when_main_arg_exist(self):
        if not self.options.save_main_arg_exists:
            return self.options.save_main_arg_exists

        if self.__main_arg['name'] in self.user_arguments:
            return True
        return False

    def save(self):
        if self.save_when_different() or self.save_when_main_arg_exist() or self.options.custom_save:
            self.settings_from_file[self.__main_arg['value']] = self.values_to_save

            write_yaml(self.file.path, self.settings_from_file)

            if self.options.show_saved:
                self.show(self.values_to_save)

        return self.configs

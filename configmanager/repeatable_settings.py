from configmanager.options import Options
from configmanager.reflection import convert_to_dict
from configmanager.settings import Settings
from configmanager.yaml import write_yaml


class RepeatableSettings(Settings):
    __main_arg = {'name': '', 'value': ''}

    def __init__(self, path, program_arguments=None, options=Options()):
        super().__init__(path, program_arguments, options)

    def __process_main_arg(self):
        for arg in self.program_arguments.to_list():
            if arg.is_main:
                self.__main_arg['name'] = arg.name
                break

        if self.__main_arg['name'] in self.user_arguments:
            self.__main_arg['value'] = getattr(self.user_arguments, self.__main_arg['name'])

    def set(self):
        self.__process_main_arg()

        if not self.exists():
            user_arguments_dict = convert_to_dict(self.user_arguments)
            try:
                self.configs[self.__main_arg['value']] = self.set_arguments_values(user_arguments_dict)
            except KeyError:
                pass
            return

        for saved_setting in self.settings_from_file:
            self.configs[saved_setting] = self.set_arguments_values(self.settings_from_file[saved_setting])

        if self.__main_arg['name'] not in self.user_arguments:
            return

        user_arguments_dict = convert_to_dict(self.user_arguments)
        self.configs[self.__main_arg['value']] = self.set_arguments_values(user_arguments_dict)

        print()

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

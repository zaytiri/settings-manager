from margument.log import throw


class SettingsProcessor:
    def __init__(self, settings, args_parser):
        """
        :param settings: A list of settings to be processed.
        :param args_parser: the instance from argsparse.ArgumentParser() previously created
        """
        self.settings = settings
        self.args_parser = args_parser

    def run(self):
        """
        This method will iterate through all the given settings and will process each one according to their specifications.
        :return: A dictionary of all settings given each containing a list of all parsed configurations from the user and/or the external file .
        """
        for setting in self.settings:
            setting.program_arguments.add_arguments(self.args_parser)

        user_arguments = None
        try:
            user_arguments = self.args_parser.parse_args()
        except AssertionError as ex:
            throw(ex)

        parsed_settings = {}
        for setting in self.settings:
            setting.user_arguments = user_arguments

            setting.program_arguments.process_arguments(self.settings)

            setting.do_commands()

            setting.set()

            parsed_settings[setting.program_arguments.__class__.__name__] = setting.save()

        return parsed_settings

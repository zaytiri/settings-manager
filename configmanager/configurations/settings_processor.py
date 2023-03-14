class SettingsProcessor:
    def __init__(self, settings, args_parser):
        self.settings = settings
        self.args_parser = args_parser

    def run(self):

        for setting in self.settings:
            setting.program_arguments.add_arguments(self.args_parser)

        user_arguments = self.args_parser.parse_args()

        parsed_settings = []
        for setting in self.settings:
            setting.user_arguments = user_arguments

            setting.program_arguments.process_arguments(self.settings)

            setting.save_condition = setting.program_arguments.save_condition()

            setting.process()

            parsed_settings.append(setting.program_arguments)

        return parsed_settings

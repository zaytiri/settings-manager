from margument.log import throw


class SettingsProcessor:
    def __init__(self, settings, args_parser):
        self.settings = settings
        self.args_parser = args_parser

    def run(self):

        for setting in self.settings:
            setting.program_arguments.add_arguments(self.args_parser)

        user_arguments = None
        try:
            user_arguments = self.args_parser.parse_args()
        except AssertionError:
            throw("Required arguments were not specified.")

        parsed_settings = {}
        for setting in self.settings:
            setting.user_arguments = user_arguments

            setting.program_arguments.process_arguments(self.settings)

            setting.do_commands()

            setting.set()

            parsed_settings[setting.program_arguments.__class__.__name__] = setting.save()

        return parsed_settings

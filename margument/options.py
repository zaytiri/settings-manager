class Options:

    def __init__(self, show_saved=False, save_different=False, save_main_arg_exists=False, custom_save=False):
        """
        :param show_saved: If True, it will show all saved configuration in the terminal, otherwise False. Default: False.
        :param save_different: If True, it will only save the configurations if they are different from the configurations already in the file. If
        False, it will not save. Default: False.
        :param save_main_arg_exists: If True, it will only save the configurations if the main argument is present in the arguments provided by the user. If
        False, it will not save. Default: False.
        :param custom_save: True or False depending on any custom condition. If True it saves, if False it will not save. Default: False.
        """
        self.show_saved = show_saved
        self.save_different = save_different
        self.save_main_arg_exists = save_main_arg_exists
        self.custom_save = custom_save


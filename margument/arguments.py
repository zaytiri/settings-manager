from margument.argument import Argument
from margument.reflection import get_class_variables


class Arguments:
    def to_list(self, is_saved=None):
        """
        It will convert all properties from this class instance into a list.
        :param is_saved: it will convert to list all properties that are set to be saved if True, otherwise if False. If None, it will convert all
        properties regardless.
        :return: a list containing all properties of this class instance.
        """
        if is_saved is None:
            is_saved = [True, False]

        class_variables = get_class_variables(self)

        arguments = []
        for var in class_variables:
            if not isinstance(var[1], Argument):
                continue

            arg = Argument.set_argument(var[1])

            if arg.to_save not in is_saved:
                continue

            arguments.append(arg)

        return arguments

    def from_list(self, arguments):
        """
        It will convert all list elements into their respective property in this class instance.
        :param arguments: a list from to_list() method
        """
        class_variables = get_class_variables(self)

        for var in class_variables:
            if not isinstance(var[1], Argument):
                continue

            arg = Argument.set_argument(var[1])

            arg_from_list = None
            for argument in arguments:
                if argument.name != arg.name:
                    continue
                arg_from_list = argument

            if arg_from_list is None:
                continue

            setattr(self, arg.name, arg_from_list)

    def add_arguments(self, args_parser):
        """
        All argument configuration from argsparse must be defined in this method. (see argsparse documentation https://docs.python.org/3/library/argparse.html#the-add-argument-method)
        :param args_parser: the instance from argsparse.ArgumentParser()
        """
        raise NotImplementedError("This method needs to be implemented.")

    def process_arguments(self, settings):
        """
        All processing of parsed user defined arguments from the argsparse must be done in this method. Processing examples: validation of fields
        from the parsed arguments from argsparse, validation of the external yaml file or definition of necessary command arguments.
        :param settings:
        """
        raise NotImplementedError("This method needs to be implemented.")
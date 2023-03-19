from configmanager.argument import Argument
from configmanager.reflection import get_class_variables


class Arguments:
    def to_list(self, is_saved=None):
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
        raise NotImplementedError("This method needs to be implemented.")

    def process_arguments(self, settings):
        raise NotImplementedError("This method needs to be implemented.")
import inspect


def get_class_variables(class_to_inspect):
    class_variables = []
    for i in inspect.getmembers(class_to_inspect):
        if not i[0].startswith('_') and not inspect.ismethod(i[1]):
            class_variables.append(i)
    return class_variables

def convert_to_dict(obj):
    vars = get_class_variables(obj)

    new_dict = {}
    for var in vars:
        new_dict[var[0]] = var[1]

    return new_dict
[![Downloads](https://pepy.tech/badge/margument)](https://pepy.tech/project/margument)

# Margument - Settings Manager

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Support](#support)
- [License](#license)
- [Status](#status)

<a name="description"></a>

## Description

Margument can manage configurations based on given program arguments using the library 'argsparse'. It can manage two types of configuration, global and repeated. It's able to save, if defined, the configurations in an external yaml file.

Repeated settings means that, in a single yaml file, the same group of configurations can be saved multiple times. Global, or non-repeated settings, means that the same group of configurations can only be saved once.

It also allows for all settings be updated individually or at the same time.

It's also able to have certain methods (commands) associated with certain arguments, meaning that when an argument is inserted, that command will be called.

<a name="features"></a>

## Features

| Feature                                          |
|:-------------------------------------------------|
| uses argsparse                                   |
| save configurations in a yaml file               |
| saved configurations can be updated individually |
| associate methods to specific argument           |


Any new features are **_very_** welcomed.

### Future features

- Currently, there's only the option to use the argsparse library as a way to write command line interfaces. In the future, it will also be able to choose another type of command-line interface writer, such as 'click' library.
- Inserting multiple values in the main argument will update specified configurations on all main arguments in RepeatableSettings.

<a name="prerequisites"></a>

## Prerequisites

[Python 3](https://www.python.org/downloads/) must be installed.

<a name="installation"></a>

## Installation

```
pip --no-cache-dir install margument
```

or,

```
pip3 --no-cache-dir install margument
```

<a name="usage"></a>

## Usage

All examples showed below are taken from the [progscheduler](https://github.com/zaytiri/program-scheduler/tree/main/progscheduler/settings) package. For a working example please refer to this package.

This library needs an instance of argsparse. Almost all argsparse configurations will not be done by this library, it only uses its features, so the following code (or similar) is needed.
```python
import argparse

args = argparse.ArgumentParser()
args.add_argument('--version', action='version', version='%(prog)s ' + str(get_version())) # optional
```

There's two types of configurations and the program can have as much as necessary. Each configuration corresponds to a different external yaml file.

- **Repeatable settings** means defining a group of configurations that can be saved multiple times, ina yaml file, under different names (main argument).
  - One of the arguments must be a main argument, meaning that this argument's value (from the user) will be the name of a specific group of configurations and can be used (by the user) to update that specific setting or delete it.
- **Non-Repeatable settings** means that all defined configurations will appear only once in the yaml file.

An Options class can also be provided containing different type of options when processing the configurations.
```python
class Manager:
    def configure_arguments(self):
        args = argparse.ArgumentParser()
        args.add_argument('--version', action='version', version='%(prog)s ' + str(get_version())) # optional

        # manage repeatable configurations
        repeatable = Repeatable()
        repeatable_config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'local.yaml') # file will be saved in the same folder as the current python file
        local_settings = RepeatableSettings(path=repeatable_config_file_path,
                                            program_arguments=repeatable,
                                            options=Options(show_saved=True, save_main_arg_exists=True))
        repeatable.are_configs_saved = local_settings.exists()
        
        # manage generic configurations
        global_config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'global.yaml')
        global_settings = NonRepeatableSettings(path=global_config_file_path,
                                                program_arguments=Generic(),
                                                options=Options(show_saved=True, save_different=True))
        
        settings_processor = SettingsProcessor([local_settings, global_settings], args) # the list of all type of configurations defined needs to be pass as argument to process all of them
        return settings_processor.run()
```

The following examples applies to all type of configuration files.
It's necessary to have a separate class for each type of configuration (repeatable or non-repeatable) where it will be defined the actual arguments necessary and processed any validations necessary. 
Each configuration class needs to inherit from the class 'Arguments' and then be added the configuration of the desired arguments using the 'Argument' class. The name of the variable, the name of the argument and the full name of the argument needs to be exactly the same.
```python
class Repeatable(Arguments):
    def __init__(self):
        self.alias = Argument(name='alias',
                              abbreviation_name='-a',
                              full_name='--alias',
                              help_message='A UNIQUE alias for the file to be scheduled. When creating and/or updating any configurations, '
                                           'this alias needs to be present.',
                              metavar="",
                              to_save=True,
                              is_main=True) # is_main = True means 'alias' is a main argument. This will set this group of configurations under this value.
```

The following method needs to be implemented, and it will add each argument into the 'argsparse'.
```python
import argparse

class Repeatable(Arguments):
    # (...)
    def add_arguments(self, args_parser):
            args_parser.add_argument(self.alias.abbreviation_name, self.alias.full_name,
                                     required=not self.are_configs_saved,
                                     help=self.alias.help_message,
                                     metavar=self.alias.metavar,
                                     default=argparse.SUPPRESS)
```

The following is an example of the definition of a global argument using commands.
```python
class Generic(Arguments):
    def __init__(self):
        self.schedules = Argument(name='schedules',
                                  abbreviation_name='-lsch',
                                  full_name='--schedules',
                                  help_message='list all saved scheduled jobs. example: -lsch',
                                  metavar="",
                                  command=Commands.get_configs, # 'Commands' is a separate class only for defining commands needed for the arguments
                                  default=False)
```

This method can also be implemented if any type of validation is necessary after the arguments are parsed and/or the configuration file has been read. In this method is also possible to associate the arguments for any method/command that needs to have arguments depending on arguments parsed.
```python
class Repeatable(Arguments):
    # (...)
    def process_arguments(self, settings):
        pass
```

When calling the configure_arguments() method, th library will process configurations, save them if needed and return all updated configurations either from the external yaml file itself or the arguments given by the user.
```python
manager = Manager()
arguments =  manager.configure_arguments()
```

<a name="support"></a>

## Support

If any problems occurs, feel free to open an issue.

<a name="license"></a>

## License

[MIT](https://choosealicense.com/licenses/mit/)

<a name="status"></a>

## Status

Currently maintaining it.
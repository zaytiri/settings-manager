# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### Status
- Added
- Changed
- Fixed
- Removed

## [1.1.1] - 2023-04-09

### Fixed
- internal syntax issue.

## [1.1.0] - 2023-04-09

### Added
- better document all methods and arguments.
- an updated readme with better explanations on how to use.
- choices (from argsparse) can be now defined in the argument.

## [1.0.3] - 2023-03-27

### Fixed
- fixed issue where an invalid configuration was being added in the repeatable settings, if there was no main argument given in the command.

## [1.0.2] - 2023-03-26

### Fixed
- fixed issue where a configuration would not be updated correctly. If given only one argument to update, all other missing arguments were being reset to their default value.

## [1.0.1] - 2023-03-21

### Changed
- changed PyPi package name to 'margument'

### Fixed
- fixed issue where it was not being validated if an argument had a command associated or not. It would give an error when the program was trying to call the argument command as 'None'.

## [1.0.0] - 2023-03-19

### Added
- first release on PyPI
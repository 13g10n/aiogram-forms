# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2022-12-30
### Changed
- Whole package was re-worked from scratch

## [0.3.0] - 2022-10-21
### Added
- Added new `PhoneNumberField` field with ability to process contact sharing
- Added utility `get_fields()` method to fetch list of form fields
- Removed `__version__` from package `__init__.py`
- Removed `EmailValidator` from validators. Please use `validators.RegexValidator(EMAIL_REGEXP)` instead
- Updated example with more details and comments
- Added some classifiers for PyPI

## [0.2.0] - 2021-08-12
### Added
- New `validation_error_message` option for fields to set custom error message in case of failed validation

### Fixes
- Fixed label bug for `ChoicesField`
- Minor type hint fixes

## [0.1.1] - 2021-06-19
### Added
- `choices` parameter in `StringField` reworked to `ChoicesField`

### Fixes
- `CHANGELOG` fixed
- `README` example fixed

## [0.1.0] - 2021-06-18
### Added
- `StringField`, `EmailField` fields added
- `ChoicesValidator`, `RegexValidator`, `EmailValidator` validators added
- Basic form processing flow added

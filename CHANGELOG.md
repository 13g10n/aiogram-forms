# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1] - 2023-04-23

### Fixed
- Fixed multiple forms issue
- Fixed mypy types to pass checks

## [1.1.0] - 2023-04-02

### Added
- New `ChoiceField` field with `ChoiceValidator` validator

### Changed
- `FormsManager.get_data` can now accept form ID as param. Form class param marked as deprecated and will be removed in next releases.
- Completed 100% tests coverage and full types coverage (mypy)

### Fixed
- Small fixes and updates for `README` example

## [1.0.1] - 2023-01-01

### Changed
- Added link to documentation website to `README.md`
- Move coverage config from `.coveragerc` to `pyproject.toml`
- Removed python 3.7 from supported versions and CI
- More tests added, to cover 100% of codebase

### Fixed
- Fix `Development Status` PyPI classifier to be `Production/Stable`
- Fixed unhandled error during `dispatcher.show` call without any form registered

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

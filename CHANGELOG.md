# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

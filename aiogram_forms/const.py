"""
Module constants
"""
# Exactly one @ sign and at least one . in the part after the @
EMAIL_REGEXP = r'[^@]+@[^@]+\.[^@]+'

# Ref: https://ihateregex.io/expr/phone/
PHONE_NUMBER_REGEXP = r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'

STATES_GROUP_SUFFIX = 'StatesGroup'

DEFAULT_VALIDATION_ERROR_MESSAGE = 'Invalid value, try again'

class TomlError(Exception): pass
class TomlValidationError(TomlError): pass
class TomlOutOfRange(TomlError): pass
class TomlNotGiven(TomlError): pass
class TomlTemplateError(TomlError): pass
class TomlParameterTypeError(TomlError): pass
class TomlInvalidOption(TomlError): pass
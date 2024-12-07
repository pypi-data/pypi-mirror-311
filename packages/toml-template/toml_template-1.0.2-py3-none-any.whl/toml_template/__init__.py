__version__ = '1.0.2'
__name__ = 'toml_template'
# don't change anything above this line

import toml as __toml
import os as __os

def load_toml_with_template(filename: str, template_filename: str | None = None) -> dict:
    from .exceptions import (
        TomlInvalidOption,
        TomlNotGiven,
        TomlOutOfRange,
        TomlParameterTypeError,
        TomlTemplateError,
        TomlValidationError
    )


    if template_filename == None:
        template_filename: str = filename.replace(".toml", ".template.toml")
    
    if not __os.path.exists(filename):
        raise TomlValidationError(f"toml file `{filename}` not found")
    
    if not __os.path.isfile(filename):
        raise TomlValidationError(f"`{filename}` must be a file")
    
    if not __os.path.exists(template_filename):
        raise TomlValidationError(f"template file `{template_filename}` not found, did you mean to give a custom `template_filename` parameter ?")
    
    if not __os.path.isfile(template_filename):
        raise TomlValidationError(f"template file `{template_filename} is not a file, did you mean to give a custom `template_filename` parameter ?")
        
    config = __toml.load(filename)
    template_config = __toml.load(template_filename)

    TYPES = {
        "int": int,
        'float': float,
        "str": str,
        'bool': bool
    }

    def _load_template(config, template_config):
        for key in template_config:
            if not key in config:
                if template_config[key]["optional"] == False:
                    raise TomlNotGiven(f"Parameter {key} is not given but it is required")
                else:
                    if type(template_config[key]) == dict:
                        config[key] = {}
                        _load_template(config[key], template_config[key])
                    else:
                        if not "default" in template_config[key]:
                            raise TomlTemplateError(f"Parameter {key} is optional, but a default is not given.")
                        config[key] = template_config[key]["default"]
                continue
            
            if type(template_config[key]) == dict:
                _load_template(config[key], template_config[key])
            
            if ("type" in template_config[key]) and (type(config[key]) != TYPES[template_config[key]["type"]]):
                raise TomlParameterTypeError(f"Parameter {key} was expected of type: {template_config[key]['type']} but got: {type(config[key])}")
            
            if ("range" in template_config[key]) and (not config[key] in range(*template_config[key]["range"])):
                raise TomlOutOfRange(f"Parameter {key} is not in range({','.join(template_config[key]["range"])})")
            
            if ("options" in template_config[key]) and (not config[key] in template_config[key]["options"]):
                raise TomlInvalidOption(f"Parameter {key} should be one of: {template_config[key]['options']} but got: {config[key]}")
    
    _load_template(config, template_config)
    return config

__all__ = [
    "load_toml_with_template"
]
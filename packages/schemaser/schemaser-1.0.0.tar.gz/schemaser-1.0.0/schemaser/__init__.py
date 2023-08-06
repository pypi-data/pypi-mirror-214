from enum import EnumMeta
import typing
import inspect
import types

__version__ = '1.0.0'

def to_json_type(instance, root:dict=None) -> dict:
    """
    Converts a Python type to JSON type.

    Arguments
    ---
    `instance` - The Python type to convert
    
    `root` - The root schema.
    """
    # v = instance
    if instance is dict: return {'type':'object', 'default': {},'properties': {}, 'additionalProperties': False}
    elif instance is list or instance is tuple: return {'type':'array', 'default': []}
    elif instance is str or instance is bytes: return {'type':'string'}
    elif instance is int: return {'type':'integer'}
    elif instance is float: return {'type':'number'}
    elif instance is bool: return {'type':'boolean'}
    elif instance is inspect._empty: return None

    elif isinstance(instance, EnumMeta):
        return {'enum': [e.value for e in instance]}
    
    elif isinstance(instance, types.GenericAlias):
        vv = typing.get_origin(instance)
        res = to_json_type(vv, root)
        if vv == list or vv==tuple:
            for arg in typing.get_args(instance):
                if isinstance(arg, types.UnionType):
                    res['items'] = to_json_type(arg, root)
                else: # tuple
                    t = to_json_type(arg, root)
                    try: res['prefixItems'].append(t)
                    except KeyError:  res['prefixItems'] = [t]
                    try:res['minItems'] += 1
                    except KeyError: res['minItems'] = 1
                    try:res['maxItems'] += 1
                    except KeyError: res['maxItems'] = 1

        return res
    
    elif typing.get_origin(instance) is typing.Union or typing.get_origin(instance) is types.UnionType:
        res = {'anyOf': []}
        for arg in typing.get_args(instance):
            t = to_json_type(arg, root)
            res['anyOf'].append(t)
        return res

    elif inspect.isclass(instance): # class
        name = instance.__module__ +'.'+ instance.__name__
        root['definitions'][name] = to_schema(instance, root)
        return {'$ref': '#/definitions/'+name}

    elif callable(instance): # function
        name = instance.__module__ +'.'+instance.__name__
        root['definitions'][name] = to_schema(instance, root)
        return {'$ref': '#/definitions/'+name}
    
    raise TypeError(f"Failed to convert '{instance.__class__.__name__}' to JSON type")

def to_schema(cls_or_func, root=None, skiparg:int=-1) -> dict:
    """
    Converts this class or function to a JSON schema
    
    Arguments
    ---
    `cls_or_func` - The class or function to convert.

    `root` - The root JSON schema.

    `skiparg` - The arg index to skip.
    """
    try:
        return cls_or_func.__schema__(cls_or_func)
    except AttributeError:
        result = {
            '$schema': 'http://json-schema.org/draft-07/schema',
            'type': 'object',
            'required': [],
            'definitions': {},
            'properties': {},
            'patternProperties': {'^\\$': True}, # Ignore $schema
            'additionalProperties': False
        }
        if root is not None:
            result = {
                'type': 'object',
                'required': [],
                'properties': {},
                'additionalProperties': False
            }

        # Parameters
        para = inspect.signature(cls_or_func).parameters
        i = 0
        for k, v in para.items():
            if i != skiparg:
                if str(v).startswith('**') == False:
                    result['properties'][k] = {}
                    prop = result['properties'][k]
                    if v.default == inspect._empty: result['required'].append(k)

                    obj = to_json_type(v.annotation, result if root is None else root) # type, definitions, refrance
                    if obj is not None:
                        for k,v in obj.items(): prop[k] = v # Merge with prop
                else:
                    result['additionalProperties'] = to_json_type(v.annotation, result if root is None else root)

        # Description
        if cls_or_func.__doc__ is not None: result['description'] = cls_or_func.__doc__
        return result

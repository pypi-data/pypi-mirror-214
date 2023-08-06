# schemaser
Converts a Python class or method to a JSON schema.

## Install
```
pip install schemaser
```

## Example
```py
import schemaser

class MyClass():
    def __init__(self, string:str=None, integer:int=None, float:float=None):
        pass

    # Custom magic method for custom schemas
    # def __schema__(self):
    #     return {}

def MyMethod(value:str, **kw:cls):
    pass

def func1(string:str, integer:int, float:float, tuple:list[str,int], array:list[str|int], object:MyClass, func:MyMethod):
    pass

# Convert func1 method to JSON Schema.
dat = schemaser.to_schema(func1)
print(dat)
```
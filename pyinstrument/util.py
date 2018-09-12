import importlib
from pyinstrument.vendor.decorator import decorator

def object_with_import_path(import_path):
    if '.' not in import_path:
        raise ValueError("Can't import '%s', it is not a valid import path" % import_path)
    module_path, object_name = import_path.rsplit('.', 1)

    module = importlib.import_module(module_path)
    return getattr(module, object_name)

def truncate(string, max_length):
    if len(string) > max_length:
        return string[0:max_length-3]+'...'
    return string

@decorator
def deprecated(func):
    ''' Marks a function as deprecated. '''
    # TODO: add a runtime warning here
    return func
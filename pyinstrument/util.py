import importlib

def object_with_import_path(import_path):
    if '.' not in import_path:
        raise ValueError("Can't import '%s', it is not a valid import path" % import_path)
    module_path, object_name = import_path.rsplit('.', 1)

    module = importlib.import_module(module_path)
    return getattr(module, object_name)


class _Missing(object):
    """ Missing object necessary for cached_property"""
    def __repr__(self):
        return 'no value'

    def __reduce__(self):
        return '_missing'

_missing = _Missing()


class cached_property(object):
    """
    Decorator originally from mitsuhiko/werkzeug.

    A decorator that converts a function into a lazy property.  The
    function wrapped is called the first time to retrieve the result
    and then that calculated result is used the next time you access
    the value"""

    def __init__(self, func, name=None, doc=None):
        self.__name__ = name or func.__name__
        self.__module__ = func.__module__
        self.__doc__ = doc or func.__doc__
        self.func = func

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        if getattr(obj, '_property_cache', None) is None:
            obj._property_cache = {}

        value = obj._property_cache.get(self.__name__, _missing)

        if value is _missing:
            value = self.func(obj)
            obj._property_cache[self.__name__] = value

        return value


def clear_property_cache(obj):
    obj._property_cache = None

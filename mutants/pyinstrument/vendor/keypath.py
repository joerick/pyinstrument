# keypath vendored from https://github.com/fictorial/keypath

# keypath is released under the BSD license:

# Copyright 2016, Fictorial LLC

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:

#     * Redistributions of source code must retain the above
#       copyright notice, this list of conditions and the following
#       disclaimer.

#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials
#       provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER “AS IS” AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
# OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
# Includes modifications by joerick, which fall under the same license.

from typing import Any
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
  """Forward call to original or mutated function, depending on the environment"""
  import os
  mutant_under_test = os.environ['MUTANT_UNDER_TEST']
  if mutant_under_test == 'fail':
    from mutmut.__main__ import MutmutProgrammaticFailException
    raise MutmutProgrammaticFailException('Failed programmatically')      
  elif mutant_under_test == 'stats':
    from mutmut.__main__ import record_trampoline_hit
    record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
    result = orig(*call_args, **call_kwargs)
    return result
  prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
  if not mutant_under_test.startswith(prefix):
    result = orig(*call_args, **call_kwargs)
    return result
  mutant_name = mutant_under_test.rpartition('.')[-1]
  if self_arg:
    # call to a class method where self is not bound
    result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
  else:
    result = mutants[mutant_name](*call_args, **call_kwargs)
  return result


def x_value_at_keypath__mutmut_orig(obj: Any, keypath: str) -> Any:
  """
  Returns value at given key path which follows dotted-path notation.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert value_at_keypath(x, 'a') == 1
    >>> assert value_at_keypath(x, 'b') == 2
    >>> assert value_at_keypath(x, 'c.d') == 3
    >>> assert value_at_keypath(x, 'c.e') == 4
    >>> assert value_at_keypath(x, 'c.f.0') == 2
    >>> assert value_at_keypath(x, 'c.f.-1') == 5
    >>> assert value_at_keypath(x, 'c.f.1.y') == 'bar'

  """
  for part in keypath.split('.'):
    if isinstance(obj, dict):
      obj = obj.get(part, {})
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part, {})
  return obj


def x_value_at_keypath__mutmut_1(obj: Any, keypath: str) -> Any:
  """
  Returns value at given key path which follows dotted-path notation.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert value_at_keypath(x, 'a') == 1
    >>> assert value_at_keypath(x, 'b') == 2
    >>> assert value_at_keypath(x, 'c.d') == 3
    >>> assert value_at_keypath(x, 'c.e') == 4
    >>> assert value_at_keypath(x, 'c.f.0') == 2
    >>> assert value_at_keypath(x, 'c.f.-1') == 5
    >>> assert value_at_keypath(x, 'c.f.1.y') == 'bar'

  """
  for part in keypath.split(None):
    if isinstance(obj, dict):
      obj = obj.get(part, {})
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part, {})
  return obj


def x_value_at_keypath__mutmut_2(obj: Any, keypath: str) -> Any:
  """
  Returns value at given key path which follows dotted-path notation.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert value_at_keypath(x, 'a') == 1
    >>> assert value_at_keypath(x, 'b') == 2
    >>> assert value_at_keypath(x, 'c.d') == 3
    >>> assert value_at_keypath(x, 'c.e') == 4
    >>> assert value_at_keypath(x, 'c.f.0') == 2
    >>> assert value_at_keypath(x, 'c.f.-1') == 5
    >>> assert value_at_keypath(x, 'c.f.1.y') == 'bar'

  """
  for part in keypath.split('XX.XX'):
    if isinstance(obj, dict):
      obj = obj.get(part, {})
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part, {})
  return obj


def x_value_at_keypath__mutmut_3(obj: Any, keypath: str) -> Any:
  """
  Returns value at given key path which follows dotted-path notation.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert value_at_keypath(x, 'a') == 1
    >>> assert value_at_keypath(x, 'b') == 2
    >>> assert value_at_keypath(x, 'c.d') == 3
    >>> assert value_at_keypath(x, 'c.e') == 4
    >>> assert value_at_keypath(x, 'c.f.0') == 2
    >>> assert value_at_keypath(x, 'c.f.-1') == 5
    >>> assert value_at_keypath(x, 'c.f.1.y') == 'bar'

  """
  for part in keypath.split('.'):
    if isinstance(obj, dict):
      obj = None
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part, {})
  return obj


def x_value_at_keypath__mutmut_4(obj: Any, keypath: str) -> Any:
  """
  Returns value at given key path which follows dotted-path notation.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert value_at_keypath(x, 'a') == 1
    >>> assert value_at_keypath(x, 'b') == 2
    >>> assert value_at_keypath(x, 'c.d') == 3
    >>> assert value_at_keypath(x, 'c.e') == 4
    >>> assert value_at_keypath(x, 'c.f.0') == 2
    >>> assert value_at_keypath(x, 'c.f.-1') == 5
    >>> assert value_at_keypath(x, 'c.f.1.y') == 'bar'

  """
  for part in keypath.split('.'):
    if isinstance(obj, dict):
      obj = obj.get(None, {})
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part, {})
  return obj


def x_value_at_keypath__mutmut_5(obj: Any, keypath: str) -> Any:
  """
  Returns value at given key path which follows dotted-path notation.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert value_at_keypath(x, 'a') == 1
    >>> assert value_at_keypath(x, 'b') == 2
    >>> assert value_at_keypath(x, 'c.d') == 3
    >>> assert value_at_keypath(x, 'c.e') == 4
    >>> assert value_at_keypath(x, 'c.f.0') == 2
    >>> assert value_at_keypath(x, 'c.f.-1') == 5
    >>> assert value_at_keypath(x, 'c.f.1.y') == 'bar'

  """
  for part in keypath.split('.'):
    if isinstance(obj, dict):
      obj = obj.get(part, None)
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part, {})
  return obj


def x_value_at_keypath__mutmut_6(obj: Any, keypath: str) -> Any:
  """
  Returns value at given key path which follows dotted-path notation.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert value_at_keypath(x, 'a') == 1
    >>> assert value_at_keypath(x, 'b') == 2
    >>> assert value_at_keypath(x, 'c.d') == 3
    >>> assert value_at_keypath(x, 'c.e') == 4
    >>> assert value_at_keypath(x, 'c.f.0') == 2
    >>> assert value_at_keypath(x, 'c.f.-1') == 5
    >>> assert value_at_keypath(x, 'c.f.1.y') == 'bar'

  """
  for part in keypath.split('.'):
    if isinstance(obj, dict):
      obj = obj.get({})
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part, {})
  return obj


def x_value_at_keypath__mutmut_7(obj: Any, keypath: str) -> Any:
  """
  Returns value at given key path which follows dotted-path notation.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert value_at_keypath(x, 'a') == 1
    >>> assert value_at_keypath(x, 'b') == 2
    >>> assert value_at_keypath(x, 'c.d') == 3
    >>> assert value_at_keypath(x, 'c.e') == 4
    >>> assert value_at_keypath(x, 'c.f.0') == 2
    >>> assert value_at_keypath(x, 'c.f.-1') == 5
    >>> assert value_at_keypath(x, 'c.f.1.y') == 'bar'

  """
  for part in keypath.split('.'):
    if isinstance(obj, dict):
      obj = obj.get(part, )
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part, {})
  return obj


def x_value_at_keypath__mutmut_8(obj: Any, keypath: str) -> Any:
  """
  Returns value at given key path which follows dotted-path notation.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert value_at_keypath(x, 'a') == 1
    >>> assert value_at_keypath(x, 'b') == 2
    >>> assert value_at_keypath(x, 'c.d') == 3
    >>> assert value_at_keypath(x, 'c.e') == 4
    >>> assert value_at_keypath(x, 'c.f.0') == 2
    >>> assert value_at_keypath(x, 'c.f.-1') == 5
    >>> assert value_at_keypath(x, 'c.f.1.y') == 'bar'

  """
  for part in keypath.split('.'):
    if isinstance(obj, dict):
      obj = obj.get(part, {})
    elif type(None) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part, {})
  return obj


def x_value_at_keypath__mutmut_9(obj: Any, keypath: str) -> Any:
  """
  Returns value at given key path which follows dotted-path notation.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert value_at_keypath(x, 'a') == 1
    >>> assert value_at_keypath(x, 'b') == 2
    >>> assert value_at_keypath(x, 'c.d') == 3
    >>> assert value_at_keypath(x, 'c.e') == 4
    >>> assert value_at_keypath(x, 'c.f.0') == 2
    >>> assert value_at_keypath(x, 'c.f.-1') == 5
    >>> assert value_at_keypath(x, 'c.f.1.y') == 'bar'

  """
  for part in keypath.split('.'):
    if isinstance(obj, dict):
      obj = obj.get(part, {})
    elif type(obj) not in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part, {})
  return obj


def x_value_at_keypath__mutmut_10(obj: Any, keypath: str) -> Any:
  """
  Returns value at given key path which follows dotted-path notation.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert value_at_keypath(x, 'a') == 1
    >>> assert value_at_keypath(x, 'b') == 2
    >>> assert value_at_keypath(x, 'c.d') == 3
    >>> assert value_at_keypath(x, 'c.e') == 4
    >>> assert value_at_keypath(x, 'c.f.0') == 2
    >>> assert value_at_keypath(x, 'c.f.-1') == 5
    >>> assert value_at_keypath(x, 'c.f.1.y') == 'bar'

  """
  for part in keypath.split('.'):
    if isinstance(obj, dict):
      obj = obj.get(part, {})
    elif type(obj) in [tuple, list]:
      obj = None
    else:
      obj = getattr(obj, part, {})
  return obj


def x_value_at_keypath__mutmut_11(obj: Any, keypath: str) -> Any:
  """
  Returns value at given key path which follows dotted-path notation.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert value_at_keypath(x, 'a') == 1
    >>> assert value_at_keypath(x, 'b') == 2
    >>> assert value_at_keypath(x, 'c.d') == 3
    >>> assert value_at_keypath(x, 'c.e') == 4
    >>> assert value_at_keypath(x, 'c.f.0') == 2
    >>> assert value_at_keypath(x, 'c.f.-1') == 5
    >>> assert value_at_keypath(x, 'c.f.1.y') == 'bar'

  """
  for part in keypath.split('.'):
    if isinstance(obj, dict):
      obj = obj.get(part, {})
    elif type(obj) in [tuple, list]:
      obj = obj[int(None)]
    else:
      obj = getattr(obj, part, {})
  return obj


def x_value_at_keypath__mutmut_12(obj: Any, keypath: str) -> Any:
  """
  Returns value at given key path which follows dotted-path notation.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert value_at_keypath(x, 'a') == 1
    >>> assert value_at_keypath(x, 'b') == 2
    >>> assert value_at_keypath(x, 'c.d') == 3
    >>> assert value_at_keypath(x, 'c.e') == 4
    >>> assert value_at_keypath(x, 'c.f.0') == 2
    >>> assert value_at_keypath(x, 'c.f.-1') == 5
    >>> assert value_at_keypath(x, 'c.f.1.y') == 'bar'

  """
  for part in keypath.split('.'):
    if isinstance(obj, dict):
      obj = obj.get(part, {})
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = None
  return obj


def x_value_at_keypath__mutmut_13(obj: Any, keypath: str) -> Any:
  """
  Returns value at given key path which follows dotted-path notation.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert value_at_keypath(x, 'a') == 1
    >>> assert value_at_keypath(x, 'b') == 2
    >>> assert value_at_keypath(x, 'c.d') == 3
    >>> assert value_at_keypath(x, 'c.e') == 4
    >>> assert value_at_keypath(x, 'c.f.0') == 2
    >>> assert value_at_keypath(x, 'c.f.-1') == 5
    >>> assert value_at_keypath(x, 'c.f.1.y') == 'bar'

  """
  for part in keypath.split('.'):
    if isinstance(obj, dict):
      obj = obj.get(part, {})
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(None, part, {})
  return obj


def x_value_at_keypath__mutmut_14(obj: Any, keypath: str) -> Any:
  """
  Returns value at given key path which follows dotted-path notation.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert value_at_keypath(x, 'a') == 1
    >>> assert value_at_keypath(x, 'b') == 2
    >>> assert value_at_keypath(x, 'c.d') == 3
    >>> assert value_at_keypath(x, 'c.e') == 4
    >>> assert value_at_keypath(x, 'c.f.0') == 2
    >>> assert value_at_keypath(x, 'c.f.-1') == 5
    >>> assert value_at_keypath(x, 'c.f.1.y') == 'bar'

  """
  for part in keypath.split('.'):
    if isinstance(obj, dict):
      obj = obj.get(part, {})
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, None, {})
  return obj


def x_value_at_keypath__mutmut_15(obj: Any, keypath: str) -> Any:
  """
  Returns value at given key path which follows dotted-path notation.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert value_at_keypath(x, 'a') == 1
    >>> assert value_at_keypath(x, 'b') == 2
    >>> assert value_at_keypath(x, 'c.d') == 3
    >>> assert value_at_keypath(x, 'c.e') == 4
    >>> assert value_at_keypath(x, 'c.f.0') == 2
    >>> assert value_at_keypath(x, 'c.f.-1') == 5
    >>> assert value_at_keypath(x, 'c.f.1.y') == 'bar'

  """
  for part in keypath.split('.'):
    if isinstance(obj, dict):
      obj = obj.get(part, {})
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part, None)
  return obj


def x_value_at_keypath__mutmut_16(obj: Any, keypath: str) -> Any:
  """
  Returns value at given key path which follows dotted-path notation.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert value_at_keypath(x, 'a') == 1
    >>> assert value_at_keypath(x, 'b') == 2
    >>> assert value_at_keypath(x, 'c.d') == 3
    >>> assert value_at_keypath(x, 'c.e') == 4
    >>> assert value_at_keypath(x, 'c.f.0') == 2
    >>> assert value_at_keypath(x, 'c.f.-1') == 5
    >>> assert value_at_keypath(x, 'c.f.1.y') == 'bar'

  """
  for part in keypath.split('.'):
    if isinstance(obj, dict):
      obj = obj.get(part, {})
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(part, {})
  return obj


def x_value_at_keypath__mutmut_17(obj: Any, keypath: str) -> Any:
  """
  Returns value at given key path which follows dotted-path notation.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert value_at_keypath(x, 'a') == 1
    >>> assert value_at_keypath(x, 'b') == 2
    >>> assert value_at_keypath(x, 'c.d') == 3
    >>> assert value_at_keypath(x, 'c.e') == 4
    >>> assert value_at_keypath(x, 'c.f.0') == 2
    >>> assert value_at_keypath(x, 'c.f.-1') == 5
    >>> assert value_at_keypath(x, 'c.f.1.y') == 'bar'

  """
  for part in keypath.split('.'):
    if isinstance(obj, dict):
      obj = obj.get(part, {})
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, {})
  return obj


def x_value_at_keypath__mutmut_18(obj: Any, keypath: str) -> Any:
  """
  Returns value at given key path which follows dotted-path notation.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert value_at_keypath(x, 'a') == 1
    >>> assert value_at_keypath(x, 'b') == 2
    >>> assert value_at_keypath(x, 'c.d') == 3
    >>> assert value_at_keypath(x, 'c.e') == 4
    >>> assert value_at_keypath(x, 'c.f.0') == 2
    >>> assert value_at_keypath(x, 'c.f.-1') == 5
    >>> assert value_at_keypath(x, 'c.f.1.y') == 'bar'

  """
  for part in keypath.split('.'):
    if isinstance(obj, dict):
      obj = obj.get(part, {})
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part, )
  return obj

x_value_at_keypath__mutmut_mutants : ClassVar[MutantDict] = {
'x_value_at_keypath__mutmut_1': x_value_at_keypath__mutmut_1, 
    'x_value_at_keypath__mutmut_2': x_value_at_keypath__mutmut_2, 
    'x_value_at_keypath__mutmut_3': x_value_at_keypath__mutmut_3, 
    'x_value_at_keypath__mutmut_4': x_value_at_keypath__mutmut_4, 
    'x_value_at_keypath__mutmut_5': x_value_at_keypath__mutmut_5, 
    'x_value_at_keypath__mutmut_6': x_value_at_keypath__mutmut_6, 
    'x_value_at_keypath__mutmut_7': x_value_at_keypath__mutmut_7, 
    'x_value_at_keypath__mutmut_8': x_value_at_keypath__mutmut_8, 
    'x_value_at_keypath__mutmut_9': x_value_at_keypath__mutmut_9, 
    'x_value_at_keypath__mutmut_10': x_value_at_keypath__mutmut_10, 
    'x_value_at_keypath__mutmut_11': x_value_at_keypath__mutmut_11, 
    'x_value_at_keypath__mutmut_12': x_value_at_keypath__mutmut_12, 
    'x_value_at_keypath__mutmut_13': x_value_at_keypath__mutmut_13, 
    'x_value_at_keypath__mutmut_14': x_value_at_keypath__mutmut_14, 
    'x_value_at_keypath__mutmut_15': x_value_at_keypath__mutmut_15, 
    'x_value_at_keypath__mutmut_16': x_value_at_keypath__mutmut_16, 
    'x_value_at_keypath__mutmut_17': x_value_at_keypath__mutmut_17, 
    'x_value_at_keypath__mutmut_18': x_value_at_keypath__mutmut_18
}

def value_at_keypath(*args, **kwargs):
  result = _mutmut_trampoline(x_value_at_keypath__mutmut_orig, x_value_at_keypath__mutmut_mutants, args, kwargs)
  return result 

value_at_keypath.__signature__ = _mutmut_signature(x_value_at_keypath__mutmut_orig)
x_value_at_keypath__mutmut_orig.__name__ = 'x_value_at_keypath'


def x_set_value_at_keypath__mutmut_orig(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split('.')
  for part in parts[:-1]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part)
  last_part = parts[-1]
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(obj) in [tuple, list]:
    obj[int(last_part)] = val
  else:
    setattr(obj, last_part, val)
  return True


def x_set_value_at_keypath__mutmut_1(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = None
  for part in parts[:-1]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part)
  last_part = parts[-1]
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(obj) in [tuple, list]:
    obj[int(last_part)] = val
  else:
    setattr(obj, last_part, val)
  return True


def x_set_value_at_keypath__mutmut_2(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split(None)
  for part in parts[:-1]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part)
  last_part = parts[-1]
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(obj) in [tuple, list]:
    obj[int(last_part)] = val
  else:
    setattr(obj, last_part, val)
  return True


def x_set_value_at_keypath__mutmut_3(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split('XX.XX')
  for part in parts[:-1]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part)
  last_part = parts[-1]
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(obj) in [tuple, list]:
    obj[int(last_part)] = val
  else:
    setattr(obj, last_part, val)
  return True


def x_set_value_at_keypath__mutmut_4(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split('.')
  for part in parts[:+1]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part)
  last_part = parts[-1]
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(obj) in [tuple, list]:
    obj[int(last_part)] = val
  else:
    setattr(obj, last_part, val)
  return True


def x_set_value_at_keypath__mutmut_5(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split('.')
  for part in parts[:-2]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part)
  last_part = parts[-1]
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(obj) in [tuple, list]:
    obj[int(last_part)] = val
  else:
    setattr(obj, last_part, val)
  return True


def x_set_value_at_keypath__mutmut_6(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split('.')
  for part in parts[:-1]:
    if isinstance(obj, dict):
      obj = None
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part)
  last_part = parts[-1]
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(obj) in [tuple, list]:
    obj[int(last_part)] = val
  else:
    setattr(obj, last_part, val)
  return True


def x_set_value_at_keypath__mutmut_7(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split('.')
  for part in parts[:-1]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(None) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part)
  last_part = parts[-1]
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(obj) in [tuple, list]:
    obj[int(last_part)] = val
  else:
    setattr(obj, last_part, val)
  return True


def x_set_value_at_keypath__mutmut_8(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split('.')
  for part in parts[:-1]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(obj) not in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part)
  last_part = parts[-1]
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(obj) in [tuple, list]:
    obj[int(last_part)] = val
  else:
    setattr(obj, last_part, val)
  return True


def x_set_value_at_keypath__mutmut_9(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split('.')
  for part in parts[:-1]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(obj) in [tuple, list]:
      obj = None
    else:
      obj = getattr(obj, part)
  last_part = parts[-1]
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(obj) in [tuple, list]:
    obj[int(last_part)] = val
  else:
    setattr(obj, last_part, val)
  return True


def x_set_value_at_keypath__mutmut_10(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split('.')
  for part in parts[:-1]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(obj) in [tuple, list]:
      obj = obj[int(None)]
    else:
      obj = getattr(obj, part)
  last_part = parts[-1]
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(obj) in [tuple, list]:
    obj[int(last_part)] = val
  else:
    setattr(obj, last_part, val)
  return True


def x_set_value_at_keypath__mutmut_11(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split('.')
  for part in parts[:-1]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = None
  last_part = parts[-1]
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(obj) in [tuple, list]:
    obj[int(last_part)] = val
  else:
    setattr(obj, last_part, val)
  return True


def x_set_value_at_keypath__mutmut_12(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split('.')
  for part in parts[:-1]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(None, part)
  last_part = parts[-1]
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(obj) in [tuple, list]:
    obj[int(last_part)] = val
  else:
    setattr(obj, last_part, val)
  return True


def x_set_value_at_keypath__mutmut_13(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split('.')
  for part in parts[:-1]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, None)
  last_part = parts[-1]
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(obj) in [tuple, list]:
    obj[int(last_part)] = val
  else:
    setattr(obj, last_part, val)
  return True


def x_set_value_at_keypath__mutmut_14(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split('.')
  for part in parts[:-1]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(part)
  last_part = parts[-1]
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(obj) in [tuple, list]:
    obj[int(last_part)] = val
  else:
    setattr(obj, last_part, val)
  return True


def x_set_value_at_keypath__mutmut_15(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split('.')
  for part in parts[:-1]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, )
  last_part = parts[-1]
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(obj) in [tuple, list]:
    obj[int(last_part)] = val
  else:
    setattr(obj, last_part, val)
  return True


def x_set_value_at_keypath__mutmut_16(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split('.')
  for part in parts[:-1]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part)
  last_part = None
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(obj) in [tuple, list]:
    obj[int(last_part)] = val
  else:
    setattr(obj, last_part, val)
  return True


def x_set_value_at_keypath__mutmut_17(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split('.')
  for part in parts[:-1]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part)
  last_part = parts[+1]
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(obj) in [tuple, list]:
    obj[int(last_part)] = val
  else:
    setattr(obj, last_part, val)
  return True


def x_set_value_at_keypath__mutmut_18(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split('.')
  for part in parts[:-1]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part)
  last_part = parts[-2]
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(obj) in [tuple, list]:
    obj[int(last_part)] = val
  else:
    setattr(obj, last_part, val)
  return True


def x_set_value_at_keypath__mutmut_19(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split('.')
  for part in parts[:-1]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part)
  last_part = parts[-1]
  if isinstance(obj, dict):
    obj[last_part] = None
  elif type(obj) in [tuple, list]:
    obj[int(last_part)] = val
  else:
    setattr(obj, last_part, val)
  return True


def x_set_value_at_keypath__mutmut_20(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split('.')
  for part in parts[:-1]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part)
  last_part = parts[-1]
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(None) in [tuple, list]:
    obj[int(last_part)] = val
  else:
    setattr(obj, last_part, val)
  return True


def x_set_value_at_keypath__mutmut_21(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split('.')
  for part in parts[:-1]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part)
  last_part = parts[-1]
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(obj) not in [tuple, list]:
    obj[int(last_part)] = val
  else:
    setattr(obj, last_part, val)
  return True


def x_set_value_at_keypath__mutmut_22(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split('.')
  for part in parts[:-1]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part)
  last_part = parts[-1]
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(obj) in [tuple, list]:
    obj[int(last_part)] = None
  else:
    setattr(obj, last_part, val)
  return True


def x_set_value_at_keypath__mutmut_23(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split('.')
  for part in parts[:-1]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part)
  last_part = parts[-1]
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(obj) in [tuple, list]:
    obj[int(None)] = val
  else:
    setattr(obj, last_part, val)
  return True


def x_set_value_at_keypath__mutmut_24(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split('.')
  for part in parts[:-1]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part)
  last_part = parts[-1]
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(obj) in [tuple, list]:
    obj[int(last_part)] = val
  else:
    setattr(None, last_part, val)
  return True


def x_set_value_at_keypath__mutmut_25(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split('.')
  for part in parts[:-1]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part)
  last_part = parts[-1]
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(obj) in [tuple, list]:
    obj[int(last_part)] = val
  else:
    setattr(obj, None, val)
  return True


def x_set_value_at_keypath__mutmut_26(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split('.')
  for part in parts[:-1]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part)
  last_part = parts[-1]
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(obj) in [tuple, list]:
    obj[int(last_part)] = val
  else:
    setattr(obj, last_part, None)
  return True


def x_set_value_at_keypath__mutmut_27(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split('.')
  for part in parts[:-1]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part)
  last_part = parts[-1]
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(obj) in [tuple, list]:
    obj[int(last_part)] = val
  else:
    setattr(last_part, val)
  return True


def x_set_value_at_keypath__mutmut_28(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split('.')
  for part in parts[:-1]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part)
  last_part = parts[-1]
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(obj) in [tuple, list]:
    obj[int(last_part)] = val
  else:
    setattr(obj, val)
  return True


def x_set_value_at_keypath__mutmut_29(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split('.')
  for part in parts[:-1]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part)
  last_part = parts[-1]
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(obj) in [tuple, list]:
    obj[int(last_part)] = val
  else:
    setattr(obj, last_part, )
  return True


def x_set_value_at_keypath__mutmut_30(obj: Any, keypath: str, val: Any):
  """
  Sets value at given key path which follows dotted-path notation.

  Each part of the keypath must already exist in the target value
  along the path.

    >>> x = dict(a=1, b=2, c=dict(d=3, e=4, f=[2,dict(x='foo', y='bar'),5]))
    >>> assert set_value_at_keypath(x, 'a', 2)
    >>> assert value_at_keypath(x, 'a') == 2
    >>> assert set_value_at_keypath(x, 'c.f.-1', 6)
    >>> assert value_at_keypath(x, 'c.f.-1') == 6
  """
  parts = keypath.split('.')
  for part in parts[:-1]:
    if isinstance(obj, dict):
      obj = obj[part]
    elif type(obj) in [tuple, list]:
      obj = obj[int(part)]
    else:
      obj = getattr(obj, part)
  last_part = parts[-1]
  if isinstance(obj, dict):
    obj[last_part] = val
  elif type(obj) in [tuple, list]:
    obj[int(last_part)] = val
  else:
    setattr(obj, last_part, val)
  return False

x_set_value_at_keypath__mutmut_mutants : ClassVar[MutantDict] = {
'x_set_value_at_keypath__mutmut_1': x_set_value_at_keypath__mutmut_1, 
    'x_set_value_at_keypath__mutmut_2': x_set_value_at_keypath__mutmut_2, 
    'x_set_value_at_keypath__mutmut_3': x_set_value_at_keypath__mutmut_3, 
    'x_set_value_at_keypath__mutmut_4': x_set_value_at_keypath__mutmut_4, 
    'x_set_value_at_keypath__mutmut_5': x_set_value_at_keypath__mutmut_5, 
    'x_set_value_at_keypath__mutmut_6': x_set_value_at_keypath__mutmut_6, 
    'x_set_value_at_keypath__mutmut_7': x_set_value_at_keypath__mutmut_7, 
    'x_set_value_at_keypath__mutmut_8': x_set_value_at_keypath__mutmut_8, 
    'x_set_value_at_keypath__mutmut_9': x_set_value_at_keypath__mutmut_9, 
    'x_set_value_at_keypath__mutmut_10': x_set_value_at_keypath__mutmut_10, 
    'x_set_value_at_keypath__mutmut_11': x_set_value_at_keypath__mutmut_11, 
    'x_set_value_at_keypath__mutmut_12': x_set_value_at_keypath__mutmut_12, 
    'x_set_value_at_keypath__mutmut_13': x_set_value_at_keypath__mutmut_13, 
    'x_set_value_at_keypath__mutmut_14': x_set_value_at_keypath__mutmut_14, 
    'x_set_value_at_keypath__mutmut_15': x_set_value_at_keypath__mutmut_15, 
    'x_set_value_at_keypath__mutmut_16': x_set_value_at_keypath__mutmut_16, 
    'x_set_value_at_keypath__mutmut_17': x_set_value_at_keypath__mutmut_17, 
    'x_set_value_at_keypath__mutmut_18': x_set_value_at_keypath__mutmut_18, 
    'x_set_value_at_keypath__mutmut_19': x_set_value_at_keypath__mutmut_19, 
    'x_set_value_at_keypath__mutmut_20': x_set_value_at_keypath__mutmut_20, 
    'x_set_value_at_keypath__mutmut_21': x_set_value_at_keypath__mutmut_21, 
    'x_set_value_at_keypath__mutmut_22': x_set_value_at_keypath__mutmut_22, 
    'x_set_value_at_keypath__mutmut_23': x_set_value_at_keypath__mutmut_23, 
    'x_set_value_at_keypath__mutmut_24': x_set_value_at_keypath__mutmut_24, 
    'x_set_value_at_keypath__mutmut_25': x_set_value_at_keypath__mutmut_25, 
    'x_set_value_at_keypath__mutmut_26': x_set_value_at_keypath__mutmut_26, 
    'x_set_value_at_keypath__mutmut_27': x_set_value_at_keypath__mutmut_27, 
    'x_set_value_at_keypath__mutmut_28': x_set_value_at_keypath__mutmut_28, 
    'x_set_value_at_keypath__mutmut_29': x_set_value_at_keypath__mutmut_29, 
    'x_set_value_at_keypath__mutmut_30': x_set_value_at_keypath__mutmut_30
}

def set_value_at_keypath(*args, **kwargs):
  result = _mutmut_trampoline(x_set_value_at_keypath__mutmut_orig, x_set_value_at_keypath__mutmut_mutants, args, kwargs)
  return result 

set_value_at_keypath.__signature__ = _mutmut_signature(x_set_value_at_keypath__mutmut_orig)
x_set_value_at_keypath__mutmut_orig.__name__ = 'x_set_value_at_keypath'

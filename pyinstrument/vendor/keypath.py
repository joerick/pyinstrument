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


def value_at_keypath(obj: Any, keypath: str) -> Any:
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


def set_value_at_keypath(obj: Any, keypath: str, val: Any):
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

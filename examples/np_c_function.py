import sys

import numpy as np

arr = np.random.randint(0, 10000, 10000)

# def print_profiler(frame, event, arg):
#     print(event, arg, getattr(arg, '__qualname__', arg.__name__), arg.__module__, dir(arg))

# sys.setprofile(print_profiler)

for i in range(10000):
    arr.cumsum()

# sys.setprofile(None)

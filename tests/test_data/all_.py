import modutil

__getattr__ = modutil.lazy___all__(__name__)

import sys

_private_attr = -13

def _private_func():
    pass

class _PrivateClass:
    pass

attr = 42

def func():
    pass

class Cls:
    pass

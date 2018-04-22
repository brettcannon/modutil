"""__doc__"""

import sys as mod


__all__ = ['Cls', 'attr', 'func']


_private_attr = '_private_attr'

__dunder__ = '__dunder__'

def _private_func():
    return '_private_func'

class _PrivateClass:
    """_PrivateClass"""

attr = 'attr'

def func():
    return 'func'

class Cls:
    """Cls"""

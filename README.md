# `modutil`

[![Build Status](https://travis-ci.org/brettcannon/modutil.svg?branch=master)](https://travis-ci.org/brettcannon/modutil)

A library for working with Python modules.

## Module Contents

### `STANDARD_MODULE_ATTRS`
A container of attribute names which all modules have.

### `ModuleAttributeError(importer_name, attribute)`
A subclass of `AttributeError` with the attributes `importer_name` and
`attribute` set to the module being searched on and the attribute being search
for, respectively.

### `lazy_import(importer_name, to_import)`
Returns the importing module and a callable for lazy importing.

The module named by `importer_name` represents the module performing the
import to help facilitate resolving relative imports.

`to_import` is an iterable of the modules to be potentially imported. Modules
may be specified either as absolute and relative names. The attribute name
that the specified module is ultimately bound to is specified in one of two
ways. First, the general case is the end of the dotted name of the module is
what the attribute name will be, e.g. `pkg.mod` will be bound to `mod` on
the importer module. Second, the `as` format of importing is also supported,
so one may say, e.g. `"pkg.mod as spam"` and have `pkg.mod` bound to the
attribute `spam` on the importer module.

This function returns a tuple of two items. The first is the importer
module itself for easy reference within itself. The second item is a callable
which is expected to be set to `__getattr__` within the importer module to allow
for lazy importing. For instance:

```python
mod, __getattr__ = lazy_import(__name__, {'sys', '.submodule',
                                          'importlib.abc as i_abc'})

def func():
    return mod.i_abc.answer == 42
```

### filtered_attrs(module, *, modules=False, private=False, dunder=False, common=False)

Return a collection of attributes on `module`.

If `modules` is false then module instances are excluded. If `private` is
false then attributes starting with, but not ending in, `_` will be
excluded. With `dunder` set to false then attributes starting and ending
with `_` are left out. The `common` argument controls whether attributes
found in `STANDARD_MODULE_ATTRS` are returned.


### calc___all__(module_name, **kwargs)

Return a sorted list of defined attributes on `module_name`.

All values specified in `**kwargs` are directly passed to `filtered_attrs()`.

Since the calculation of what attributes should be included is done eagerly, the
function should be called as late as possible in the construction of the module
to make sure to include all appropriate attributes. For example, the expected
usage is:
```python
# __all__ is defined at the end of the module.

# ... module contents ...

__all__ = module.calc___all__(__name__)
```

### filtered_dir(module_name, *, additions={}, **kwargs)

Return a callable appropriate for `__dir__()`.

All values specified in `**kwargs` get passed directly to `filtered_attrs()`.
The `additions` argument should be an iterable which is added to the final
results.

### `chained__getattr__(importer_name, *getattrs)`
Return a callable which calls the chain of `__getattr__` functions in sequence.

Any raised `ModuleAttributeError` which matches `importer_name` and the
attribute being searched for will be caught and the search will continue.
All other exceptions will be allowed to propagate. If no callable successfully
returns a value, `ModuleAttributeError` will be raised.

Example usage is:
```python
mod, import_getattr = modutil.lazy_import(__name__, {'mod'})
all_getattr = modutil.lazy___all__(__name__)
__getattr__ = modutil.chained___getattr__(__name__, import_getattr, all_getattr)
del import_getattr, all_getattr
```

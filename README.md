[![Build Status](https://travis-ci.org/brettcannon/modutil.svg?branch=master)](https://travis-ci.org/brettcannon/modutil)

A library for working with Python modules.

# Module Contents

## `COMMON_MODULE_ATTRS`
A container of attribute names which all modules have.

## `lazy___all__(importer_name)`
Returns a callable which will lazily create `__all__` for `importer_name`.

After being set as the `__getattr__` function for `importer_name`, the first
request for `__all__` will look through the attributes of the module and add
them to all, ignoring:

- Modules (under the assumption that they were imported and not part of the
  module's API).
- Attributes which start with `_` but do not end in `_` (meaning that they
  have a leading underscore and thus are private to the module).
- Any attribute whose name is in `COMMON_MODULE_ATTRS` (under the assumption
  that attributes common to all modules are not meant to be a part of `__all__`).

`__all__` will be set after its first access and thus will not be dynamically
updated if future attributes are added to the module.

## `lazy_import(importer_name, to_import)`
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

## `create_AttributeError(module_name, attribute)`
Create an instance of `AttributeError` with its arguments set as attributes
with the same name. A reasonable message is also provided automatically.

## `chained__getattr__(importer_name, *getattrs)`
Return a callable which calls the chain of `__getattr__` functions in sequence.

If a callable raises an `AttributeError` as created by `create_AttributeError()`
then the next callable will be called. If no callable finds the attribute then
the last `AttributeError` raised will be allowed to propagate. Any
`AttributeError` not created by `create_AttributeError()` will immediately
propagate to avoid masking of non-purposeful `AttributeError` exceptions.

Example usage is:
```python
mod, import_getattr = modutil.lazy_import(__name__, {'mod'})
all_getattr = modutil.lazy___all__(__name__)
__getattr__ = modutil.chained___getattr__(__name__, import_getattr, all_getattr)
del import_getattr, all_getattr
```

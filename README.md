A library for working with Python modules.

# Module Contents

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

"""Help for working with modules."""
__version__ = "1.1.dev2"

import importlib
import importlib.machinery
import importlib.util
import types


def create_AttributeError(module_name, attribute):
    """Create an instance of AttributeError with extra attributes.

    Both module_name and 'attribute' will be set as attributes on the returned
    instance of AttributeError with the same name.
    """
    # Changes to the attributes must be updated as appropriate in
    # chained___getattr__() as well.
    message = f'module {module_name!r} has no attribute {attribute!r}'
    exc = AttributeError(message)
    exc.module_name = module_name
    exc.attribute = attribute
    return exc


def lazy_import(importer_name, to_import):
    """Return the importing module and a callable for lazy importing.

    The module named by importer_name represents the module performing the
    import to help facilitate resolving relative imports.

    to_import is an iterable of the modules to be potentially imported (absolute
    or relative). The `as` form of importing is also supported,
    e.g. `pkg.mod as spam`.

    This function returns a tuple of two items. The first is the importer
    module for easy reference within itself. The second item is a callable to be
    set to `__getattr__`.
    """
    module = importlib.import_module(importer_name)
    import_mapping = {}
    for name in to_import:
        importing, _, binding = name.partition(' as ')
        if not binding:
            _, _, binding = importing.rpartition('.')
        import_mapping[binding] = importing

    def __getattr__(name):
        if name not in import_mapping:
            raise create_AttributeError(importer_name, name)
        importing = import_mapping[name]
        # imortlib.import_module() implicitly sets submodules on this module as
        # appropriate for direct imports.
        imported = importlib.import_module(importing,
                                           module.__spec__.parent)
        setattr(module, name, imported)
        return imported

    return module, __getattr__


COMMON_MODULE_ATTRS = frozenset(['__all__', '__builtins__', '__cached__',
                                 '__doc__', '__file__', '__loader__',
                                 '__name__', '__package__', '__spec__',
                                 '__getattr__'])


def _unique_objects(module):
    """Create a sorted list of objects defined in the module."""
    attrs = []
    for name in dir(module):
        # Ignore what every module has.
        if name in COMMON_MODULE_ATTRS:
            continue
        # Leave out private attributes.
        elif name.startswith('_') and not name.endswith('_'):
            continue
        # Imported modules should be skipped.
        elif isinstance(getattr(module, name), types.ModuleType):
            continue
        attrs.append(name)
    attrs.sort()
    return attrs


def lazy___all__(importer_name):
    """Lazily calculate __all__ for importer_name."""
    module = importlib.import_module(importer_name)

    def __getattr__(name):
        if name != '__all__':
            raise create_AttributeError(importer_name, name)
        all_ = _unique_objects(module)
        module.__all__ = all_
        return all_

    return __getattr__


def chained___getattr__(importer_name, *getattrs):
    """Create a callable which calls each __getattr__ in sequence.

    Any AttributeError exception not created by create_AttributeError() will
    immediately be propagated. Otherwise the exception will be caught and
    calling functions will continue. If the attribute is never found then the
    last AttributeError raised will be what is propagated.
    """
    def __getattr__(name):
        """Call each __getattr__ function in sequence."""
        last_exc = None
        for getattr_ in getattrs:
            try:
                return getattr_(name)
            except AttributeError as exc:
                # Checks tied to create_AttributeError().
                if getattr(exc, 'module_name', None) == importer_name:
                    if getattr(exc, 'attribute', None) == name:
                        last_exc = exc
                        continue
                raise exc
        else:
            raise last_exc

    return __getattr__

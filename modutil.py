"""Help for working with modules."""
__version__ = "1.1.dev1"

import importlib
import importlib.machinery
import importlib.util
import types


def _create_AttributeError(module_name, attribute):
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
            raise _create_AttributeError(importer_name, name)
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
            raise _create_AttributeError(importer_name, name)
        all_ = _unique_objects(module)
        module.__all__ = all_
        return all_

    return __getattr__

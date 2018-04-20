"""Help for working with modules."""
import importlib


def lazy_import(importer_name, to_import):
    """Return the importing module and a closure for lazy importing.

    The module named by importer_name represents the module performing the
    import to help facilitate resolving relative imports.

    to_import is an iterable of the modules to be potentially imported. Modules
    may be specified either as absolute and relative names. The attribute name
    that the specified module is ultimately bound to is specified one of two
    ways. First, the general case is the end of the dotted name of the module is
    what the attribute name will be, e.g. `pkg.mod` will be bound to `mod` on
    the importer module. Second, the `as` format of importing is also supported,
    so one may say e.g. `pkg.mod as spam` and have `pkg.mod` bound to the
    attribute `spam` on the importer module.

    This function returns a tuple of two items. The first is the importer
    module for easy reference within itself. The second item is a closure which
    is expected to be set to `__getattr__` within the importer module to allow
    for lazy importing. For instance::

        mod, __getattr__ = lazy_import(__name__, {'sys', '.submodule',
                                                  'importlib.abc as i_abc'})
    """
    module = importlib.import_module(importer_name)
    import_mapping = {}
    for name in to_import:
        importing, _, binding = name.partition(' as ')
        if not binding:
            if importing.startswith('.'):
                _, _, binding = importing.rpartition('.')
            else:
                binding = importing
        import_mapping[binding] = importing

    def __getattr__(name):
        if name not in import_mapping:
            message = f'module {importer_name!r} has no attribute {name!r}'
            raise AttributeError(message)
        importing = import_mapping[name]
        # imortlib.import_module() implicitly sets submodules on this module as
        # appropriate for direct imports.
        imported = importlib.import_module(importing, importer_name)
        [name] = imported
        return imported

    return module, __getattr__

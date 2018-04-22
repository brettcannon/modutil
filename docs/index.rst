.. modutil documentation master file, created by
   sphinx-quickstart on Sun Apr 22 15:21:13 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to modutil's documentation!
===================================

.. image:: https://img.shields.io/pypi/v/nine.svg
    :alt: PyPI

A library for working with Python modules.


Module Contents
---------------

.. attribute:: STANDARD_MODULE_ATTRS

    A container of attribute names which all modules have.


.. exception:: ModuleAttributeError(importer_name, attribute)

    A subclass of :exc:`AttributeError` with the attributes *importer_name* and
    *attribute* set to the module being searched on and the attribute being
    searched for, respectively.


.. function:: lazy_import(importer_name, to_import)

    Returns the importing module and a callable for lazy importing.

    The module named by *importer_name* represents the module performing the
    import to help facilitate resolving relative imports.

    *to_import* is an iterable of the modules to be potentially imported.
    Modules may be specified either as absolute and relative names. The
    attribute name that the specified module is ultimately bound to is specified
    in one of two ways. First, the general case is the end of the dotted name of
    the module is what the attribute name will be, e.g. ``pkg.mod`` will be
    bound to ``mod`` on the importer module. Second, the ``as`` format of
    importing is also supported, so one may say, e.g. ``"pkg.mod as spam"`` and
    have ``pkg.mod`` bound to the attribute ``spam`` on the importer module.

    This function returns a tuple of two items. The first is the importer
    module itself for easy reference within itself. The second item is a callable
    which is expected to be set to ``__getattr__`` within the importer module to
    allow for lazy importing. For instance::

        mod, __getattr__ = lazy_import(__name__, {'sys', '.submodule',
                                                'importlib.abc as i_abc'})

        def func():
            return mod.i_abc.answer == 42

    .. warning::
        This function should only be used in code where start-up time is
        paramount (e.g. large CLI apps). Otherwise using this function will lead
        to import errors occurring lazily and with a less helpful traceback.


.. function:: filtered_attrs(module, *, modules=False, private=False, dunder=False, common=False)

    Return a collection of attributes on *module*.

    If *modules* is false then module instances are excluded. If *private* is
    false then attributes starting with, but not ending in, ``_`` will be
    excluded. With *dunder* set to false then attributes starting and ending
    with ``_`` are left out. The *common* argument controls whether attributes
    found in :attr:`STANDARD_MODULE_ATTRS` are returned.


.. function:: calc___all__(module_name, **kwargs)

    Return a sorted list of defined attributes on *module_name*.

    All values specified in ``**kwargs`` are directly passed to
    :func:`filtered_attrs`.

    Since the calculation of what attributes should be included is done eagerly,
    the function should be called as late as possible in the construction of the
    module to make sure to include all appropriate attributes. For example, the
    expected usage is::

        # __all__ is defined at the end of the module.

        # ... module contents ...

        __all__ = module.calc___all__(__name__)


.. function:: filtered_dir(module_name, *, additions={}, **kwargs)

    Return a callable appropriate for :func:`__dir__`.

    All values specified in ``**kwargs`` get passed directly to
    :func:`filtered_attrs`. The *additions* argument should be an iterable which
    is added to the final results.


.. function:: chained__getattr__(importer_name, *getattrs)

    Return a callable which calls the chain of :func:`__getattr__` functions in
    sequence.

    Any raised :exc:`ModuleAttributeError` which matches *importer_name* and the
    attribute being searched for will be caught and the search will continue.
    All other exceptions will be allowed to propagate. If no callable successfully
    returns a value, :exc:`ModuleAttributeError` will be raised.

    Example usage is::

        mod, import_getattr = modutil.lazy_import(__name__, {'mod'})
        all_getattr = modutil.lazy___all__(__name__)
        __getattr__ = modutil.chained___getattr__(__name__, import_getattr, all_getattr)
        del import_getattr, all_getattr

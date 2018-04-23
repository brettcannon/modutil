# modutil

[![Build Status](https://travis-ci.org/brettcannon/modutil.svg?branch=master)](https://travis-ci.org/brettcannon/modutil)
[![Read the Docs](https://img.shields.io/readthedocs/modutil.svg)](https://modutil.readthedocs.io/)

A library for working with Python modules. The highlights are:

* ``lazy_import()`` provides a way to do lazy import for large CLI apps.
* ``calc___all__()`` allows you to no longer have to manually maintain a
  module's :attr:`__all__`.
* ``filtered_dir()`` has ``dir()`` only show the relevant attributes of your
  module.

For these and other features of the library, please visit the
[documentation](https://modutil.readthedocs.io/).

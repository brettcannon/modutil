import pytest

import modutil

import importlib
import sys


def manage_module(name):
    module = importlib.import_module(name)
    yield module
    clear_out = set()
    for name in sys.modules.keys():
        if name.startswith('tests.test_data'):
            clear_out.add(name)
    for name in clear_out:
        del sys.modules[name]

@pytest.fixture
def lazy_package():
    yield from manage_module('tests.test_data.lazy_pkg')

@pytest.fixture
def lazy_module():
    yield from manage_module('tests.test_data.lazy_mod')


def test_absolute_import(lazy_module):
    looking_for = 'tests.test_data.A'
    assert looking_for not in sys.modules
    module = lazy_module.trigger_A()
    assert module.__name__ == looking_for
    assert looking_for in sys.modules


def test_relative_import(lazy_module):
    looking_for = 'tests.test_data.B'
    assert looking_for not in sys.modules
    module = lazy_module.trigger_B()
    assert module.__name__ == looking_for
    assert looking_for in sys.modules


def test_name_rebinding(lazy_module):
    looking_for = 'tests.test_data.C'
    assert looking_for not in sys.modules
    module = lazy_module.trigger_C()
    assert module.__name__ == looking_for
    assert looking_for in sys.modules


def test_module_not_reimported(lazy_module):
    looking_for = 'tests.test_data.A'
    assert looking_for not in sys.modules
    module = lazy_module.trigger_A()
    assert module.answer == 42
    module.answer = -13
    module = lazy_module.trigger_A()
    assert module.answer == -13


def test_AttributeError(lazy_module):
    looking_for = 'tests.test_data.A'
    assert looking_for not in sys.modules
    module = lazy_module.trigger_A()
    with pytest.raises(AttributeError):
        module.is_not_there


def test_lazy_in_package(lazy_package):
    assert lazy_package.__name__ == 'tests.test_data.lazy_pkg'
    looking_for = 'tests.test_data.A'
    assert looking_for not in sys.modules
    module = lazy_package.trigger_A()
    assert module.__name__ == looking_for
    assert looking_for in sys.modules

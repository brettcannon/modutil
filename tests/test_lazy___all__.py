import pytest

import modutil

from .test_data import all_ as all_module


def test_nothing_private():
    assert '_private_attr' not in all_module.__all__
    assert '_private_func' not in all_module.__all__
    assert '_PrivateClass' not in all_module.__all__


def test_ignoring_modules():
    assert 'modutil' not in all_module.__all__
    assert 'sys' not in all_module.__all__


def test_public_stuff():
    assert all_module.__all__ == sorted(['Cls', 'attr', 'func'])


def test_AttributeError():
    with pytest.raises(AttributeError):
        all_module.does_not_exist

import modutil

from .test_data import all_


def test_defaults():
    __dir__ = modutil.filtered_dir(all_.__name__)
    # Implicitly tests that the result is sorted.
    assert __dir__() == all_.__all__


def test_arg_passthrough():
    __dir__ = modutil.filtered_dir(all_.__name__, dunder=True)
    assert '__dunder__' in __dir__()


def test_additions():
    __dir__ = modutil.filtered_dir(all_.__name__, additions={'stuff'})
    result = __dir__()
    expected = sorted(all_.__all__ + ['stuff'])
    assert result == expected

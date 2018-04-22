import modutil

from .test_data import all_


def test_attrs():
    __all__ = modutil.calc___all__(all_.__name__)
    assert set(__all__) == modutil.filtered_attrs(all_)


def test_arg_passthrough():
    __all__ = modutil.calc___all__(all_.__name__, dunder=True)
    assert '__dunder__' in __all__


def test_sorted_result():
    __all__ = modutil.calc___all__(all_.__name__)
    assert sorted(__all__) == __all__


def test_defaults():
    __all__ = modutil.calc___all__(all_.__name__)
    assert __all__ == all_.__all__

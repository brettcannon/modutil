import modutil

from .test_data import all_


def check(attr, arg):
    kwargs = {arg: True}
    attrs = modutil.filtered_attrs(all_, **{arg: True})
    assert attr in attrs
    attrs = modutil.filtered_attrs(all_, **{arg: False})
    assert attr not in attrs


def test_no_modules():
    check('mod', 'modules')


def test_no_private_attrs():
    check('_private_func', 'private')
    check('_PrivateClass', 'private')
    attrs = modutil.filtered_attrs(all_, private=False, dunder=True)
    assert '__dunder__' in attrs


def test_no_dunder_attrs():
    check('__dunder__', 'dunder')
    attrs = modutil.filtered_attrs(all_, private=True, dunder=False)
    assert '_private_func' in attrs


def test_no_common_attrs():
    attrs = modutil.filtered_attrs(all_, common=True, dunder=True)
    assert '__doc__' in attrs
    attrs = modutil.filtered_attrs(all_, common=False, dunder=True)
    assert '__doc__' not in attrs
    assert '__dunder__' in attrs


def test_defaults():
    attrs = modutil.filtered_attrs(all_)
    assert attrs == frozenset(all_.__all__)

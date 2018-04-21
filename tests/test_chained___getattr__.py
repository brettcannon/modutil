import pytest

import modutil


def test_create_AttributeError():
    name = __name__
    attr = 'some_attr'
    exc = modutil.create_AttributeError(name, attr)
    assert isinstance(exc, AttributeError)
    assert exc.module_name == name
    assert exc.attribute == attr


def test_ordering_preserved():
    def getattr1(name):
        raise modutil.create_AttributeError(__name__, name)

    def getattr2(name):
        return 42

    def getattr3(name):
        raise RuntimeError('should never be reached')

    chain = modutil.chained___getattr__(__name__, getattr1, getattr2, getattr3)
    assert chain('does_not_matter') == 42


def test_unexpected_AttributeError_propagates():
    message = 'raised by other code'

    def getattr1(name):
        raise modutil.create_AttributeError(__name__, name)

    def getattr2(name):
        raise AttributeError(message)

    def getattr3(name):
        raise RuntimeError('should never be reached')

    chain = modutil.chained___getattr__(__name__, getattr1, getattr2, getattr3)
    with pytest.raises(AttributeError) as exc_info:
        chain('does_not_matter')
    assert str(exc_info.value) == message


def test_last_AttributeError_raised():
    expected = modutil.create_AttributeError(__name__, 'does_not_matter')

    def getattr1(name):
        raise modutil.create_AttributeError(__name__, name)

    def getattr2(name):
        raise expected

    chain = modutil.chained___getattr__(__name__, getattr1, getattr2)
    with pytest.raises(AttributeError) as exc_info:
        chain('does_not_matter')
    assert exc_info.value is expected

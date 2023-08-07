import pytest
from wc_shortcodes.registry import CodesRegistry, CodeDefinition
from wc_shortcodes import parser


def test_initialization():
    CodesRegistry()


def test_add():
    r = CodesRegistry()

    r.add('first', lambda x: x.content)

    assert r.has('first')
    assert not r.has('second')

    with pytest.raises(KeyError):
        r.add('first', lambda x: x.name)

    resolvable = parser.Entity('first', 0, 0, None, 'result')
    assert r.get('first').resolver(resolvable) == 'result'

    r.remove('first')
    r.add('first', lambda x: x.name)

    assert r.get('first').resolver(resolvable) == 'first'


def test_decorator():
    r = CodesRegistry()

    @r.register('first')
    def resolver(e):
        return e.content

    resolvable = parser.Entity('first', 0, 0, None, 'result')
    assert r.get('first').resolver(resolvable) == 'result'

    with pytest.raises(AssertionError):
        @r.register(' ')
        def emptynamed(e):
            return e.content

    with pytest.raises(AssertionError):
        r.register()(lambda x: '')

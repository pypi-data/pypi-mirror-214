from typing import List
from wc_shortcodes import transformer, registry, parser


C = [
    'Text.\n',
    '<p>Inside paragraph</p>\n',
    # 2
    '[just-simple]',

    '\n<div>',
    # 4
    '''[shortcode1
        attr
        attr2="46"
        attr-4="89"
    ]''',
    # 5
    '''[no-tag-nested attr5]
    Otherdata here
    [/no-tag-nested]''',

    '\ncontent\n',

    # 7
    '[namespaced:one attr attr2="46" attr-4="8\"43\"9"]',
    '[/shortcode1]',

    # 9
    '''[no-tag]
    Otherdata here
    [/no-tag]''',

    'Multiline\n',

    # 11
    '''[namespaced:one
        attr
        attr2="46"
        attr-4='8"43"9'
        attr_4="56'45's" "attr5" 6 attr7=46
        attr8="34r" юникод=другой
    ]''',

    ''' [&#39;just-simple&#39;] ''',
    ''' [] ''',
    ''' [ ] ''',

    '</div>',
]
TEXT = ''.join(C)


def test_transform():
    r = registry.CodesRegistry()
    counter = {}

    # Empty registry results in same output
    assert transformer.transform(r, TEXT) == TEXT

    @r.register('just-simple')
    def simple(entity, context={}):
        return 'simple'

    # Only one simple code
    assert transformer.transform(r, TEXT) == ''.join(
        C[:2] + ['simple'] + C[3:]
    )

    @r.register('namespaced:one', multiple=True)
    def namespaced(entities: List[parser.Entity], context={}):
        counter['nmsp'] = counter.get('nmsp', 0) + 1
        counter['nmsp-count'] = counter.get('nmsp-count', 0) + len(entities)

        return [
            e.attributes.get('юникод', '') + e.attributes['attr2']
            for e in entities
        ]

    # Both namespaced should be resolved.
    # Even if one of them is inside the content of `shortcode1`.
    # Since `shortcode1` not registered his "content" should not be identified
    # as "content".
    assert transformer.transform(r, TEXT) == ''.join(
        C[:2] + ['simple'] + C[3:7] + ['46'] + C[8:11] + ['другой46'] + C[12:]
    )
    assert counter['nmsp'] == 1
    assert counter['nmsp-count'] == 2

    @r.register()
    def shortcode1(entity, context={}):
        return entity.content

    counter = {}
    assert transformer.transform(r, TEXT) == ''.join(
        C[:2] + ['simple'] + C[3:4] + C[5:7]
        +
        ['46']
        +
        C[9:11] + ['другой46'] + C[12:]
    )
    # Even when item is a dependency - namespace launches only once.
    assert counter['nmsp'] == 1
    assert counter['nmsp-count'] == 2

    r.remove('shortcode1')

    @r.register('shortcode1', autoresolve_content=False)
    def sho1(entity, context={}):
        return entity.content

    counter = {}
    assert transformer.transform(r, TEXT) == ''.join(
        C[:2] + ['simple'] + C[3:4] + C[5:8] + C[9:11] + ['другой46'] + C[12:]
    )
    # Since now shortcode1's content is not autoresolvable namespace will
    # be used only once.
    assert counter['nmsp'] == 1
    assert counter['nmsp-count'] == 1

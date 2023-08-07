import re
from typing import Iterator
from wc_shortcodes import parser
from pprint import pprint


TEXT_ONE = '''
Some text. And again one.

<p>Inside paragraph</p>

<div>[shortcode1]</div>

[no-tag]

[namespaced:one]
'''

TEXT_ATTRIBUTES = '''
Some text. And again one.

<p>Inside paragraph</p>

<div>[shortcode1 attr attr2="46" attr-4="89"]</div>

[no-tag  attr attr2="46" attr-4="89"]

[namespaced:one attr attr2="46" attr-4="89"]
'''

TEXT_CONTENT = '''
Some text. And again one.

<p>Inside paragraph</p>

<div>
[shortcode1 attr attr2="46" attr-4="89"]
Data 1
[/shortcode1]
</div>

[no-tag]
Otherdata here
[/no-tag]

[namespaced:one attr attr2="46" attr-4="89"]
'''

TEXT_CONTENT_NESTED = r'''
Some text. And again one.

<p>Inside paragraph</p>

[just-simple]

<div>
[shortcode1
    attr
    attr2="46"
    attr-4="89"
]
[no-tag-nested attr5]
Otherdata here
[/no-tag-nested]

[namespaced:one attr attr2="46" attr-4="8\"43\"9"]
[/shortcode1]

[no-tag]
Otherdata here
[/no-tag]

Multiline:

[namespaced:two
    attr
    attr2="46"
    attr-4='8"43"9'
    attr_4="56'45's" "attr5" 6 attr7=46
    attr8="34r" юникод=другой
]
</div>

'''


def test_codes_lookup():
    assert len(parser.find_entities(TEXT_ONE)) == 3
    assert len(parser.find_entities(TEXT_ATTRIBUTES)) == 3
    assert len(parser.find_entities(TEXT_CONTENT)) == 3

    nested = parser.find_entities(TEXT_CONTENT_NESTED)

    # Because nested inside content should not be automatically parsed:
    assert len(nested) == 4
    assert nested[0].content == ''
    assert tuple(x.name for x in nested) == (
        'just-simple', 'shortcode1', 'no-tag', 'namespaced:two'
    )

    internal_content = nested[1].content

    assert len(parser.find_entities(internal_content)) == 2


def test_attributes_resolvement():
    nested = parser.find_entities(TEXT_CONTENT_NESTED)
    attributable = nested[3]
    attrs = attributable.attributes
    items = list(attrs.items())

    assert len(attributable.attributes) == 9

    # Interpolation check
    assert attrs['attr-4'] == '8"43"9'
    assert attrs['attr_4'] == "56'45's"
    assert attrs['attr7'] == '46'
    assert 'attr5' in attrs
    assert '"attr5"' not in attrs

    # Ordering check:
    assert items[4][0] == 'attr5'
    assert items[5][0] == '6'
    assert items[8][0] == 'юникод'

    # Unicode support:
    assert 'юникод' in attrs
    assert attrs['юникод'] == 'другой'

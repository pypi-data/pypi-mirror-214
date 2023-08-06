from maestro.utils.parsing import (
    parse_color,
    extract_index,
    BIG_ENOUGH,
    make_doc_page,
)

from maestro.model.documentation import (
    Section,
    Text,
)

import pytest

def test_extract_index_no_clear_index():
    names = [
    'Fatboy Slim ft. Bootsy Collins - Weapon Of Choice [Official 4k Video]',
    'Bessie',
    'Stella Jang (스텔라장) - Reality Blue Official M_V',
    'Earth, Wind & Fire - September (Official Video)',
    '1st Sword - 10',
    'Richter - Autumn 3',
    ]
    for name in names:
        assert extract_index(name) == (BIG_ENOUGH, name)

def test_extract_index_finds_valid_index():
    assert (    extract_index('Interstellar OST 01 Dreaming Of The Crash')
             ==           (1, 'Interstellar OST Dreaming Of The Crash'))

    assert (    extract_index('07 Le Tour de France en Diligence - Camille')
             ==              (7, 'Le Tour de France en Diligence - Camille'))

    assert (    extract_index('Cars 2 - 01. You Might Think')
             ==           (1, 'Cars 2 - You Might Think'))

def small_diff(va, vb):
    return all(abs(x-y) < 1/256 for x, y in zip(va, vb))

def test_parse_color():
    assert parse_color('#ff0000') == (1, 0, 0)
    assert small_diff(parse_color('#0080ff'), (0, 0.5, 1))
    assert small_diff(parse_color('#1ab247'), (0.1, 0.7, 0.28))
    with pytest.raises(ValueError):
        assert parse_color('#abc')
    with pytest.raises(ValueError):
        assert parse_color('abcdef')
    with pytest.raises(ValueError):
        assert parse_color('#abcdeg')

def test_make_doc_page_with_titles():
    doc = make_doc_page(
    '''
    # Title
    Bla bla
    bla
    ## Part 1
    Wow
    ## Part 2
    Cool

    That too
    ### Detail
    Just a
    small thing
    ## Part 3
    The end
    ''')

    expected = Section(Text('Title'),
                       Text('Bla bla bla'),
                       Section(Text('Part 1'),
                               Text('Wow')),
                       Section(Text('Part 2'),
                               Text('Cool'),
                               Text('That too'),
                               Section(Text('Detail'),
                                       Text('Just a small thing'))),
                       Section(Text('Part 3'),
                               Text('The end')))
    assert doc == expected

def test_make_doc_page_list_of_items():
    doc = make_doc_page(
    '''
    # Title
    Some text and a list:
    - one
    - two
    and the rest

    Next paragraph
    ''')

    expected = Section(Text('Title'),
                       Text('Some text and a list:'),
                       Text('- one'),
                       Text('- two and the rest'),
                       Text('Next paragraph'),
                       )
    assert doc == expected

def test_make_doc_page_code_block():
    doc = make_doc_page(
    '''
    # Title
    Codeblock
    ```
    this is

    - the code
        indented

    ```
    ''')

    expected = Section(Text('Title'),
                       Text('Codeblock'),
                       Text('this is', '', '- the code', '    indented', '')
                       )
    assert doc == expected
    code_block = doc.elements[1]
    assert code_block.style == 'codeblock'

def test_make_doc_page_no_section_raises_value_error():
    with pytest.raises(ValueError):
        make_doc_page('abc')

def test_make_doc_page_level2section_before_level1section_raises_value_error():
    with pytest.raises(ValueError):
        make_doc_page('''
        ## Bug

        # And

        ### What
        ''')

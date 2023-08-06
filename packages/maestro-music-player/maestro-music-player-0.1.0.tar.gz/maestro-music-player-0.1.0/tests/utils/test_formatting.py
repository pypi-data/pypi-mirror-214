from maestro.utils.formatting import (
    format_time,
    format_plural,
    make_selection_tag,
    with_selection_tag,
)

def test_format_time():
    assert format_time(60*1000) == '01:00'
    assert format_time((12*60+34)*1000) == '12:34'
    assert format_time((49*60+7)*1000) == '49:07'

def test_make_selection_tag():
    assert make_selection_tag(True) != make_selection_tag(False)

def test_with_selection_tag():
    text = 'Hello, world !'
    assert with_selection_tag(text, False) == text
    with_tag = with_selection_tag(text, True)
    assert text in with_tag

def test_format_plural():
    assert format_plural(0, 'car', 'cars') == '0 cars'
    assert format_plural(1, 'car', 'cars') == '1 car'
    assert format_plural(2, 'car', 'cars') == '2 cars'
    assert format_plural(355, 'car', 'cars') == '355 cars'

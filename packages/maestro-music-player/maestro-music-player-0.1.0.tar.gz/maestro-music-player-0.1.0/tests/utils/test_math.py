from maestro.utils.math import clamp, none_to_default

import pytest

def test_clamp_in_range():
    assert clamp(0, 200, 23) == 23

def test_clamp_smaller():
    assert clamp(0, 12, -3) == 0

def test_clamp_bigger():
    assert clamp(0, 10, 345) == 10

def test_clamp_invalid_bounds():
    with pytest.raises(ValueError):
        clamp(10, 1, 23)

def test_none_to_default():
    assert none_to_default(345, 12) == 345
    assert none_to_default(None, 12) == 12

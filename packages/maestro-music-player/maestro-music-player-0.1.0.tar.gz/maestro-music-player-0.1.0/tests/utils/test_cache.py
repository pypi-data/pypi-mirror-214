
from maestro.utils.cache import simple_cache, cached_attr

import pytest


@pytest.fixture
def stupid():

    @simple_cache
    class Stupid:

        def set_seed(self, seed):
            self.seed = seed

        @cached_attr('magic', lambda s: s.seed)
        def compute_magic(self):
            return 13*self.seed - 5

    return Stupid()

@pytest.fixture
def crash():

    @simple_cache
    class Crash:

        def set_seed(self, seed):
            self.seed = seed

        @cached_attr('magic', lambda s: s.seed)
        def compute_magic(self):
            raise Exception('Impossible to compute')

    Crash.set_cache({1: 8, 2: 21})

    return Crash()

def test_attribute_undefined_if_compute_not_called(stupid):
    with pytest.raises(AttributeError):
        stupid.magic

def test_compute_value_and_set_attribute(stupid):
    stupid.set_seed(1)
    assert stupid.compute_magic() == 8
    assert stupid.magic == 8
    stupid.set_seed(2)
    assert stupid.magic == 8
    assert stupid.get_cache() == {1: 8}


def test_cache_bypasses_computation_if_value_in_cache(crash):
    crash.set_seed(1)
    crash.compute_magic()
    crash.compute_magic()
    crash.compute_magic()
    assert crash.magic == 8
    crash.set_seed(2)
    crash.compute_magic()
    crash.compute_magic()
    assert crash.magic == 21
    crash.set_seed(3)
    with pytest.raises(Exception):
        crash.compute_magic()


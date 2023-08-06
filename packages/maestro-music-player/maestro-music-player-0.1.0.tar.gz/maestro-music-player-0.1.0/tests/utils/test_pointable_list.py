from maestro.utils.pointable_list import PointableList

import pytest #type: ignore


def test_plist_append_and_length():
    pl = PointableList()
    assert len(pl) == 0
    pl.append(0)
    pl.append(2)
    pl.append(3)
    assert len(pl) == 3

def test_plist_clear():
    pl = PointableList()
    size = 12
    for i in range(size):
        pl.append(i)
    assert len(pl) == size
    pl.clear()
    assert len(pl) == 0

def test_plist_extend():
    pl = PointableList()
    size = 15
    pl.extend([i for i in range(size)])
    assert len(pl) == size

def test_plist_getitem():
    pl = PointableList()
    size = 12
    pl.extend([i*i for i in range(size)])
    assert pl[3] == 9
    assert pl[11] == 121

def test_plist_setitem():
    pl = PointableList()
    size = 8
    pl.extend([5*i for i in range(size)])
    assert pl[4] == 20
    pl[4] = 12
    for _ in range(23):
        pl.append(0)
    assert pl[4] == 12

def test_plist_del_item():
    pl = PointableList(fallback_item=-1)
    size = 8
    pl.extend([i for i in range(size)])
    assert pl[4] == 4
    del pl[4]
    del pl[4]
    del pl[4]
    assert pl[4] == 7
    del pl[4]
    with pytest.raises(IndexError):
        pl[4]

def test_plist_shuffle():
    pl = PointableList()
    ptr = pl.new_pointer()
    pl.extend(['b', 'c', 'a', 'e', 'd'])
    ptr.set_index(3)
    pl.shuffle()
    assert sorted(pl) == ['a', 'b', 'c', 'd', 'e']
    assert ptr.index == 0

def test_plist_simple_ptr():
    pl = PointableList(fallback_item=-1)
    ptr = pl.new_pointer()
    assert ptr.index is None
    assert ptr.value == -1
    pl.extend(['a', 'b', 'c', 'd', 'e'])
    assert ptr.index == 0
    assert ptr.value == 'a'

def test_plist_simple_null_ptr():
    pl = PointableList(fallback_item=-1)
    ptr = pl.new_pointer(loop=True, avoid_null_state=False)
    assert ptr.index is None
    assert ptr.value == -1
    pl.extend(['a', 'b', 'c', 'd', 'e'])
    assert ptr.index is None

def test_plist_ptr_fallback():
    pl = PointableList(fallback_item='z')
    ptr = pl.new_pointer()
    assert ptr.value == 'z'
    pl.extend(['a', 'b', 'c', 'd', 'e'])
    assert ptr.value == 'a'

def test_plist_ptr_setindex():
    pl = PointableList()
    ptr = pl.new_pointer()
    assert ptr.index == None
    pl.extend(['a', 'b', 'c', 'd', 'e'])
    assert ptr.value == 'a'
    ptr.set_index(4)
    assert ptr.value == 'e'
    with pytest.raises(IndexError):
        ptr.set_index(-1)
    assert ptr.value == 'e'
    with pytest.raises(IndexError):
        ptr.set_index(5)
    assert ptr.value == 'e'

def test_plist_ptr_does_not_move_when_adding_items():
    pl = PointableList()
    ptr = pl.new_pointer()
    pl.extend(['a', 'b', 'c', 'd', 'e'])
    assert ptr.value == 'a'
    pl.append('z')
    pl.append('q')
    assert ptr.value == 'a'

def test_plist_ptr_inc_dec():
    pl = PointableList()
    pl.extend(['a', 'b', 'c', 'd', 'e'])
    ptr = pl.new_pointer()
    ptr.increment()
    ptr.increment()
    ptr.increment()
    assert ptr.index == 3
    assert ptr.value == 'd'
    ptr.increment(-1)
    ptr.increment(-1)
    assert ptr.index == 1
    assert ptr.value == 'b'

def test_plist_ptr_dec_from_null():
    pl = PointableList()
    pl.extend(['a', 'b', 'c', 'd', 'e'])
    ptr = pl.new_pointer(loop=True, avoid_null_state=False)
    assert ptr.index == None
    ptr.increment(-1)
    assert ptr.index == 4

def test_plist_ptr_inc_block_at_bounds():
    pl = PointableList()
    pl.extend(['a', 'b', 'c', 'd', 'e'])
    ptr = pl.new_pointer()
    for _ in range(100):
        ptr.increment()
    assert ptr.index == 4
    assert ptr.value == 'e'
    ptr.increment(-100)
    assert ptr.index == 0
    assert ptr.value == 'a'

def test_plist_ptr_loop():
    pl = PointableList()
    pl.extend(['a', 'b', 'c', 'd', 'e'])
    ptr = pl.new_pointer(loop=True)
    ptr.increment(3)
    assert ptr.index == 3
    assert ptr.value == 'd'
    ptr.increment(16)
    assert ptr.index == 4
    assert ptr.value == 'e'
    ptr.increment(-23)
    assert ptr.index == 1
    assert ptr.value == 'b'

def test_plist_ptr_can_be_null():
    pl = PointableList()
    pl.extend(['a', 'b', 'c', 'd', 'e'])
    ptr = pl.new_pointer(loop=True, avoid_null_state=False)
    ptr.increment(1)
    assert ptr.index == 0
    ptr.increment(5)
    assert ptr.index is None
    ptr.increment(1)
    assert ptr.index == 0
    assert ptr.value == 'a'

def test_plist_ptr_reset():
    pl = PointableList()
    pl.extend(['a', 'b', 'c', 'd', 'e'])
    ptr = pl.new_pointer(avoid_null_state=True)
    ptr.increment(3)
    assert ptr.index == 3
    ptr.reset()
    assert ptr.index == 0

def test_plist_ptr_reset_to_null():
    pl = PointableList()
    pl.extend(['a', 'b', 'c', 'd', 'e'])
    ptr = pl.new_pointer(loop=True, avoid_null_state=False)
    ptr.increment(4)
    assert ptr.index == 3
    ptr.reset()
    assert ptr.index is None

def test_plist_ptr_invalid_set_index():
    pl = PointableList()
    pl.extend(['a', 'b', 'c', 'd', 'e'])
    ptr = pl.new_pointer()
    with pytest.raises(TypeError):
        ptr.set_index(None)

def test_plist_invalid_ptr_params():
    pl = PointableList()
    pl.extend(['a', 'b', 'c', 'd', 'e'])
    with pytest.raises(ValueError):
        ptr = pl.new_pointer(avoid_null_state=False)

def test_plist_ptr_move_when_list_modifies():
    pl = PointableList()
    size = 8
    pl.extend([i for i in range(size)])
    ptr = pl.new_pointer()
    assert ptr.index == 0
    assert ptr.value == 0
    ptr.set_index(5)
    assert ptr.index == 5
    assert ptr.value == 5
    del pl[7]
    assert ptr.index == 5
    del pl[3]
    assert ptr.index == 4
    del pl[3]
    assert ptr.index == 3
    assert ptr.value == 5
    ptr.increment()
    assert ptr.index == 4
    assert ptr.value == 6
    del pl[3]
    assert ptr.index == 3
    assert ptr.value == 6
    del pl[3]
    assert ptr.index == 2
    assert ptr.value == 2
    pl.clear()
    assert ptr.index is None

def test_plist_loop_ptr_move_when_list_modifies():
    pl = PointableList()
    size = 8
    ptr = pl.new_pointer(loop=True, avoid_null_state=False)
    pl.extend([i for i in range(size)])
    assert ptr.index is None
    ptr.set_index(5)
    assert ptr.index == 5
    assert ptr.value == 5
    del pl[7]
    del pl[3]
    del pl[3]
    assert ptr.index == 3
    assert ptr.value == 5
    ptr.increment()
    assert ptr.index == 4
    assert ptr.value == 6
    del pl[3]
    assert ptr.index == 3
    assert ptr.value == 6
    del pl[3]
    assert ptr.index is None

def test_delete_with_just_one_item():
    pl = PointableList()
    ptr = pl.new_pointer()
    pl.append('just one')
    assert ptr.value == 'just one'
    del pl[ptr.index]
    assert ptr.index is None

def test_delete_with_just_one_item_loop():
    pl = PointableList()
    ptr = pl.new_pointer(loop=True, avoid_null_state=False)
    pl.append('just one')
    assert ptr.index is None
    del pl[0]
    assert ptr.index is None

def test_increment_ptr_when_list_empty():
    pl = PointableList()
    ptr = pl.new_pointer()
    ptr.increment()
    ptr.increment()
    assert ptr.index is None

def test_ptr_callback_called_when_list_changes():
    pl = PointableList()
    flag = []
    ptr = pl.new_pointer(on_change=lambda index: flag.append(index))
    pl.append('a')
    assert flag == [None, 0]

def test_plist_recreate():
    pl = PointableList()
    pl.extend(range(20))
    ptr = pl.new_pointer()
    ptr.increment(10)
    assert ptr.value == 10
    assert len(pl) == 20
    pl.recreate([-2, -5, -12])
    assert ptr.value == -2
    assert len(pl) == 3

def test_plist_select():
    pl = PointableList()
    pl.extend(['a', 'b', 'c', 'd', 'e'])
    ptr = pl.new_pointer(loop=True, avoid_null_state=False)
    assert not pl.is_selected(ptr.index)
    ptr.set_index(0)
    assert not pl.is_selected(ptr.index)
    ptr.select()
    assert pl.is_selected(ptr.index)
    expected = [
        ('a', True),
        ('b', False),
        ('c', False),
        ('d', False),
        ('e', False),
    ]
    for res, exp in zip(pl.iter_with_metadata(), expected):
        assert res == exp

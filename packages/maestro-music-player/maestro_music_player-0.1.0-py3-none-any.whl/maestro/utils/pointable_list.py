#!/usr/bin/env python3

# This file is part of maestro, a keyboard-driven configurable music player.
# Copyright (C) 2022  Baptiste Lambert (Blaireau) rabbitstemplate@disroot.org
#
# Maestro is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from maestro.utils.math import clamp

import random


class PointableListElement:

    def __init__(self, data):
        self.data = data
        self.selected = False

    def select(self, select=True, invert=False):
        if invert:
            self.selected = not self.selected
        else:
            self.selected = select


class PointableList:

    def __init__(self, fallback_item=None, on_change=lambda *x:None):
        self._fallback_item = fallback_item
        self._data = []
        self._pointers = []
        self._on_change_callback = on_change

    def select(self, index: int, *args, **kwargs):
        self._data[index].select(*args, **kwargs)

    def select_all(self, *args, **kwargs):
        for elem in self._data:
            elem.select(*args, **kwargs)

    @property
    def selected_items(self):
        return (elem.data for elem in self._data if elem.selected)

    def is_selected(self, index):
        if index is None:
            return False
        return self._data[index].selected

    def delete_selected(self):
        i = 0
        while i < len(self):
            if self.is_selected(i):
                del self._data[i]
                self._update_ptrs(decrement_above=i)
            else:
                i += 1
        self._on_change_callback()

    def clear(self):
        self._data = []
        for ptr in self._pointers:
            ptr.set_index(None)
        self._on_change_callback()

    def shuffle(self):
        random.shuffle(self._data)
        for ptr in self._pointers:
            ptr.reset()
        self._on_change_callback()

    def _update_ptrs(self, *args, **kwargs):
        for ptr in self._pointers:
            ptr._update(*args, **kwargs)

    def append(self, element_data):
        element = PointableListElement(element_data)
        self._data.append(element)
        self._update_ptrs()
        self._on_change_callback()

    def extend(self, elements_data):
        elements = (PointableListElement(d) for d in elements_data)
        self._data.extend(elements)
        self._update_ptrs()
        self._on_change_callback()

    def recreate(self, elements_data):
        self._data = []
        for ptr in self._pointers:
            ptr.set_index(None)
        self.extend(elements_data)

    def new_pointer(self, loop=False, avoid_null_state=True,
                          on_change=lambda *x:None):
        '''
        create a new item pointer for the list.

        If loop is set, incrementing the pointer past the end of the list
        will make it start from the beggining (and vice-versa).
        Otherwise, the pointer will be blocked at the list’s boundaries.

        If avoid_null_state is False, the pointer can be in a "null state"
        even if the list is not empty.
        This setting implies loop = True.
        '''
        ptr = PointableListPointer(self, loop, avoid_null_state, on_change)
        self._pointers.append(ptr)
        return ptr

    def __getitem__(self, index):
        if index is None:
            return self._fallback_item
        return self._data[index].data

    def __setitem__(self, index, value):
        self._data[index].data = value
        self._on_change_callback()

    def __delitem__(self, index):
        del self._data[index]
        self._update_ptrs(decrement_above=index)
        self._on_change_callback()

    def __len__(self):
        return len(self._data)

    def __iter__(self): # pragma: no cover
        return (elem.data for elem in self._data)

    def iter_with_metadata(self):
        return ((elem.data, elem.selected) for elem in self._data)

    def __repr__(self):
        return repr(self._data)

    def __str__(self): # pragma: no cover
        return str(self._data)


class PointableListPointer:
    '''do not instantiate directly !
    use PointableList.new_pointer()'''

    def __init__(self, pointable_list, loop=False, avoid_null_state=True,
                       on_change=lambda *x:None):
        if not loop and not avoid_null_state:
            raise ValueError('loop should be True when avoid_null_state '
                             'is disabled')
        self._pointed_list = pointable_list
        self.loop = loop
        self.avoid_null_state = avoid_null_state
        self.callback = on_change
        if len(pointable_list) == 0 or not avoid_null_state:
            self._index = None
        else:
            self._index = 0
        self.do_callback()

    def do_callback(self):
        self.callback(self.index)

    def _update(self, decrement_above=None):
        if self._index is None:
            if self.avoid_null_state:
                # something has been added to the list and we must point to it
                self.increment()
            return
        if decrement_above is None:
            # nothing special, we probably just added new things at the end
            return
        if self._index > decrement_above:
            # an item bellow us was deleted, we shift
            return self.increment(-1)
        if self._index == decrement_above == len(self._pointed_list):
            # our item was deleted and it was the last in the list
            if self.avoid_null_state and len(self._pointed_list) > 0:
                # if the list is not empty, we go back
                return self.increment(-1)
            # otherwise, we point to None
            return self.set_index(None)

    def reset(self):
        if self.avoid_null_state and len(self._pointed_list) != 0:
            self.set_index(0)
        else:
            self.set_index(None)

    def increment(self, increment=1):
        if increment == 0 or len(self._pointed_list) == 0:
            return
        if self._index is None:
            if increment > 0:
                index = -1
            else:
                index = len(self._pointed_list)
        else:
            index = self._index
        if self.loop:
            mod = len(self._pointed_list)
            if not self.avoid_null_state:
                mod += 1
            index = (index + increment) % mod
            if not self.avoid_null_state and index == len(self._pointed_list):
                index = None
        else:
            index = clamp(0, len(self._pointed_list) - 1, index + increment)
        self.set_index(index)

    def set_index(self, new_index):
        if new_index is None:
            if self.avoid_null_state and len(self._pointed_list) != 0:
                raise TypeError('PointableListPointer cannot be set to None.\n'
                                'Use avoid_null_state=False to allow this '
                                'behavior.')
            else:
                self._index = None
        else:
            if 0 <= new_index < len(self._pointed_list):
                self._index = new_index
            else:
                raise IndexError('Pointer index out of range')
        self.do_callback()

    @property
    def index(self):
        return self._index

    @property
    def value(self):
        return self._pointed_list[self._index]

    def select(self, *args, **kwargs):
        if self._index is not None:
            self._pointed_list.select(self._index, *args, **kwargs)



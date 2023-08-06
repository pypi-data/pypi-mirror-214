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
from maestro.utils.pointable_list import PointableList



class FocusPanel(PointableList):

    def __init__(self, *args, name=None, metadata=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.metadata = metadata
        self._focus_ptr = self.new_pointer()

    @property
    def focused_item(self):
        return self._focus_ptr.value

    @property
    def focused_index(self):
        return self._focus_ptr.index

    @focused_index.setter
    def focused_index(self, value):
        self._focus_ptr.set_index(value)

    def move_focus(self, increment: int):
        self._focus_ptr.increment(increment)

    def select_focused(self, *args, **kwargs):
        self._focus_ptr.select(*args, **kwargs)



class QueuePanel(FocusPanel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._playing_ptr = self.new_pointer(loop=True, avoid_null_state=False)
        self._loop_queue = False

    @property
    def loop(self):
        return self._loop_queue

    @loop.setter
    def loop(self, value):
        self._loop_queue = value

    @property
    def playing_item(self):
        return self._playing_ptr.value

    @property
    def playing_index(self):
        return self._playing_ptr.index

    @playing_index.setter
    def playing_index(self, value):
        self._playing_ptr.set_index(value)

    def next(self):
        self._playing_ptr.increment(1)
        if self._playing_ptr.index is None and self.loop:
            self._playing_ptr.increment(1)

    def previous(self):
        self._playing_ptr.increment(-1)
        if self._playing_ptr.index is None and self.loop:
            self._playing_ptr.increment(-1)

    def stop_playing(self):
        self._playing_ptr.reset()

    def delete_focused(self):
        if len(self) > 0 and self.focused_index is not None:
            del self[self.focused_index]

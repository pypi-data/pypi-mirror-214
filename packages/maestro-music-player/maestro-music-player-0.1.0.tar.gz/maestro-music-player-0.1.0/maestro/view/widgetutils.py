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

from kivy.animation import Animation
from kivy.uix.recycleview import RecycleView
from kivy.uix.widget import Widget
from kivy.lang import Builder

from kivy.properties import (
    AliasProperty,
    NumericProperty,
)

from pathlib import Path

kv_file = Path(__file__).parent / 'widgetutils.kv'
Builder.load_file(kv_file.as_posix())


class CProperties(Widget):

    def __init__(self, *args, **kwargs):
        kivy_props = {}
        custom_props = {}
        for key, value in kwargs.items():
            if key in self.properties() or key.startswith('__'):
                kivy_props[key] = value
            else:
                custom_props[key] = value
        super().__init__(**kivy_props)
        for keyvalue in custom_props.items():
            setattr(self, *keyvalue)


class ColorProgressBar(CProperties):

    def __init__(self, **kwargs):
        self._value = 0.
        super().__init__(**kwargs)

    def _get_value(self):
        return self._value

    def _set_value(self, value):
        value = max(0, min(self.max, value))
        if value != self._value:
            self._value = value
            return True

    value = AliasProperty(_get_value, _set_value)

    def get_norm_value(self):
        d = self.max
        if d == 0:
            return 0
        return self.value / float(d)

    def set_norm_value(self, value):
        self.value = value * self.max

    value_normalized = AliasProperty(get_norm_value, set_norm_value,
                                     bind=('value', 'max'), cache=True)

    max = NumericProperty(100.)


class RecycleScroll(RecycleView):

    def scroll_to_item(self, item_index: int | None):
        if item_index is None:
            return
        vh = self.height
        total_h = self.recycle_layout.height
        hidden_height = total_h - vh
        view_bot = self.scroll_y * hidden_height
        view_top = view_bot + vh
        item_top = total_h - (self.children_height+self.spacing)*item_index
        item_bot = item_top - self.children_height
        scroll_y = self.scroll_y
        if hidden_height > 0:
            if item_bot < view_bot:
                scroll_y = item_bot / hidden_height
            elif item_top > view_top:
                scroll_y = (item_top - vh) / hidden_height
            Animation(scroll_y=scroll_y, d=self.scroll_delay).start(self)
        else:
            self.scroll_y = 1.0


class RecycleScrollGrid(RecycleScroll):

    def scroll_to_item(self, item_index: int | None):
        if item_index is None:
            return
        super().scroll_to_item(item_index // self.cols)


class RecycleScrollList(RecycleScroll):
    pass

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

from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.properties import (
    StringProperty,
)
from maestro.view.appdocrender import AppDocRender

import maestro.view.widgetutils

from maestro.utils.formatting import (
    with_selection_tag,
    make_selection_tag,
    format_plural,
)


class Panel(Screen):

    @property
    def columns(self):
        return 1


class CollectionPanel(Panel):

    def set_data(self, panel_data):
        self.scroll_grid.data = [
            {
                'name': with_selection_tag(a.name, sel),
                'cover': a.cover,
                'selected': sel,
                'focused': i == panel_data.focused_index,
                'alt': i%2 == 0,
            } for i, (a, sel) in enumerate(panel_data.iter_with_metadata())]
        Clock.schedule_once(
            lambda t: self.scroll_grid.scroll_to_item(panel_data.focused_index))

    @property
    def columns(self):
        return self.scroll_grid.cols


class AlbumPanel(Panel):
    album_name = StringProperty()
    album_cover = StringProperty()
    album_info = StringProperty()

    def set_data(self, panel_data):
        album = panel_data.metadata
        self.album_name = album.name
        self.album_cover = album.cover
        self.album_info = format_plural(len(album), 'song', 'songs')
        self.scroll_list.data = [
            {
                'name': with_selection_tag(s.name, sel),
                'index': str(i+1),
                'selected': sel,
                'focused': i == panel_data.focused_index,
                'alt': i%2 == 0,
            } for i, (s, sel) in enumerate(panel_data.iter_with_metadata())]
        Clock.schedule_once(
            lambda t: self.scroll_list.scroll_to_item(panel_data.focused_index))


class QueuePanel(Panel):

    def set_data(self, panel_data):
        self.scroll_list.data = [
            {
                'name': with_selection_tag(s.name, sel),
                'album_name': s.album.name,
                'selected': sel,
                'index': str(i+1),
                'selected': sel,
                'focused': i == panel_data.focused_index,
                'playing': i == panel_data.playing_index,
                'alt': i%2 == 0,
            } for i, (s, sel) in enumerate(panel_data.iter_with_metadata())]
        Clock.schedule_once(
            lambda t: self.scroll_list.scroll_to_item(panel_data.focused_index))


class DocPanel(Panel):

    def set_data(self, data):
        pass

    def render_doc(self, doc):
        renderer = AppDocRender()
        doc.render(renderer)
        self.scroll_view.clear_widgets()
        self.scroll_view.add_widget(renderer.result)

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
from typing import Iterable

from enum import Enum

from maestro.model.panels import FocusPanel, QueuePanel
from maestro.model.collection import Album, Song, MusicCollection


class AppMode(Enum):
    NORMAL = 1
    COMMAND = 2
    POPUP = 4


class Application:
    """
    Models the state of the maestro application

    This class DOES NOT contain anything about:
        - how the app is displayed
        - how the music is played
    """

    def __init__(self):
        """
        Initialise the application from a music collection
        """
        self._collection_panel = FocusPanel(name='collection',
                                            fallback_item=Album.empty())
        self._album_panel = FocusPanel(name='album',
                                       fallback_item=Song.dummy())
        self._queue = QueuePanel(name='queue',
                                 fallback_item=Song.dummy())
        self._doc_panel = FocusPanel(name='documentation',
                                     fallback_item=None)
        self._panels = [self._collection_panel, self._album_panel,
                        self._queue, self._doc_panel]
        self._current_panel = self._collection_panel
        self._album_panel.metadata = Album.empty()
        self._mode = AppMode.NORMAL
        self._collection = MusicCollection()

    def set_collection(self, collection):
        self._collection = collection
        self._collection_panel.recreate(collection)
        self._album_panel.clear()
        self._queue.clear()

    def switch_to_mode(self, new_mode: AppMode):
        self._mode = new_mode

    @property
    def mode(self):
        return self._mode

    @property
    def loop(self):
        return self._queue.loop

    @loop.setter
    def loop(self, value):
        self._queue.loop = value

    @property
    def collection(self):
        return self._collection

    @property
    def playing_song(self):
        return self._queue.playing_item

    @property
    def playing_index(self):
        return self._queue.playing_index

    @playing_index.setter
    def playing_index(self, value):
        self._queue.playing_index = value

    @property
    def focused_item(self):
        return self._current_panel.focused_item

    @property
    def focused_index(self):
        return self._current_panel.focused_index

    @focused_index.setter
    def focused_index(self, value):
        self._current_panel.focused_index = value

    @property
    def queue_length(self):
        return len(self._queue)

    @property
    def current_panel(self):
        return self._current_panel

    @property
    def song_getter(self):
        return self._collection.get_song_by_uid

    @property
    def queue_playlist_data(self):
        return [song.uid for song in self._queue]

    def show_panel(self, panel_name: str):
        """
        Show a given panel (set it as the current panel)
        panel_name should be one of 'collection', 'album' or 'queue'
        Otherwise, raise a ValueError
        """
        match panel_name:
            case 'collection':
                self._current_panel = self._collection_panel
            case 'album':
                self._current_panel = self._album_panel
            case 'queue':
                self._current_panel = self._queue
            case 'documentation':
                self._current_panel = self._doc_panel
            case _:
                raise ValueError(f'Invalid panel name {panel_name}')

    def add_focused_to_queue(self):
        if self._current_panel is self._collection_panel:
            self._queue.extend(self.focused_item)
        else:
            self._queue.append(self.focused_item)

    def add_selection_to_queue(self):
        if self._current_panel is self._collection_panel:
            for album in self._collection_panel.selected_items:
                self._queue.extend(album)
        else:
            self._queue.extend(self.current_panel.selected_items)

    def add_playlist_to_queue(self, playlist_songs: Iterable[Song]):
        self._queue.extend(playlist_songs)

    def show_album_in_album_panel(self, album: Album):
        self._album_panel.metadata = album
        self._album_panel.recreate(album)

    def move_focus(self, increment: int):
        self._current_panel.move_focus(increment)

    def play_next(self):
        self._queue.next()

    def play_previous(self):
        self._queue.previous()

    def stop_playing(self):
        self._queue.stop_playing()

    def clear_queue(self):
        self._queue.clear()

    def shuffle_queue(self):
        self._queue.shuffle()

    def load_songuid_cache(self, cache):
        cache_size = len(cache)
        Song.set_cache(cache)

    @property
    def songcache_was_modified(self):
        return Song.is_modified()

    def get_songuid_cache(self):
        return Song.get_cache()

    # @command("newtag",
    #          (
    #              lambda name: '/' not in name,
    #              'a name for the tag'
    #          )
    # )
    # def create_new_tag(self, tag_name: str):
    #     try:
    #         self.tag_manager.create_tag(tag_name)
    #     except KeyError:
    #         raise CommandError(f'The tag {tag_name} already exists')

    # @command("tag",
    #          (
    #              lambda selection: selection in ["all", "current", "selection"],
    #              "one of 'all', 'current', 'selection'"
    #          ),
    #          (
    #              lambda name: '/' not in name,
    #              'a tag name'
    #          ),
    #          (
    #              lambda value: True,
    #              'a value for the tag'
    #          )
    # )
    # def edit_tag(self, selection: str, tag_name: str, value: str):
    #     try:
    #         tag = self.tag_manager.get_tag(tag_name)
    #     except KeyError:
    #         raise CommandError(f'Tag {tag_name} does not exist')
    #     match selection:
    #         case 'selection':
    #             songs = self.collection.iter_selected_songs()
    #         case _:
    #             songs = self.root.panel_manager.current_screen.get_selection(selection)
    #     for song in songs:
    #         tag.add_song(song.uid, value)
    #     self.root.panel_manager.current_screen.rebuild()

    # @command("get", (lambda i: i == "playing-title", "playing-title"))
    # def get_info(self, info):
    #     match info:
    #         case "playing-title":
    #             raise CommandError(self.current_song_name)

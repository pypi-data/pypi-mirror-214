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

import trio

from pathlib import Path

from maestro.systemutils.systemtools import (
        get_file_uid,
)
from maestro.utils.cache import simple_cache, cached_attr
from maestro.utils.parsing import extract_index
from maestro.utils.ressources import DUMMY_COVER, DUMMY_NAME, EMPTY_ALBUM_NAME


class ComputationNotReady(Exception):
    pass


@simple_cache
class Song:

    @classmethod
    def dummy(cls):
        dummy = cls(Path(""), Album.empty())
        dummy.name = DUMMY_NAME
        dummy.__dummy = True
        return dummy

    @property
    def is_dummy(self):
        return self.__dummy

    @property
    def uid(self):
        if self.is_dummy:
            return None
        if self._uid is None:
            self._compute_uid()
        return self._uid

    @property
    def album(self):
        return self._album

    @property
    def album_name(self):
        return self._album.name

    @cached_attr('_uid', lambda s: s.path.as_posix())
    def _compute_uid(self):
        return get_file_uid(self.path)

    @property
    def cover(self):
        return self._album.cover

    def __init__(self, path: Path, parent_album: 'Album', index_clues=True):
        self._uid = None
        self.path: Path = path
        if index_clues:
            self.index_clue, self.name = extract_index(path.stem)
        else:
            self.index_clue = 0
            self.name = path.stem
        self._album = parent_album
        self.__dummy = False
        self._selected = False


class Album:

    @classmethod
    def empty(cls):
        return cls(EMPTY_ALBUM_NAME)

    def __init__(self, name: str, cover=None):
        self.name: str = name
        self._songs: list[Song] = []
        self._cover: None | Path = cover

    @property
    def cover(self) -> str:
        if self._cover is None:
            return DUMMY_COVER.as_posix()
        return self._cover.as_posix()

    def __iter__(self): # pragma: no cover
        return iter(self._songs)

    def __len__(self):
        return len(self._songs)

    def __getitem__(self, index): # pragma: no cover
        return self._songs[index]

    def sort(self):
        self._songs.sort(key=lambda s: s.name)
        self._songs.sort(key=lambda s: s.index_clue)

    def append(self, song):
        self._songs.append(song)

    def extend(self, songs):
        self._songs.extend(songs)


class MusicCollection:

    @classmethod
    def dummy(cls):
        return cls()

    def __init__(self):
        self._albums: list[Album] = []
        self.song_table_ready = True
        self.song_table_progress = 0
        self._songs_table: dict[str, Song] = {}

    def add_album(self, album: Album):
        self._albums.append(album)
        self.song_table_ready = False

    def add_albums(self, albums: Iterable[Album]):
        self._albums.extend(albums)
        self.song_table_ready = False

    async def build_song_table(self):
        total = len(self)
        for i, album in enumerate(self):
            for song in album:
                self.add_song_to_table(song)
                await trio.sleep(0)
            self.song_table_progress = i / total
        self.song_table_ready = True

    def add_song_to_table(self, song: Song):
        self._songs_table[song.uid] = song

    def get_song_by_uid(self, uid: str):
        if not self.song_table_ready:
            raise ComputationNotReady(f'{self.song_table_progress*100:.0f} %')
        return self._songs_table.get(uid)

    def sort(self, recursive=True):
        if recursive:
            for album in self._albums:
                album.sort()
        self._albums.sort(key=lambda a: a.name)

    def __iter__(self): # pragma: no cover
        return iter(self._albums)

    def __len__(self):
        return len(self._albums)

    def __getitem__(self, index): # pragma: no cover
        return self._albums[index]

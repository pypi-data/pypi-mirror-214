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
from typing import Callable, Iterable

from maestro.model.collection import Album, Song
from maestro.utils.ressources import (
    MUSIC_EXTENSIONS,
    COVER_EXTENSIONS,
    MASTER_COVER_NAME,
    FALLBACK_COVER,
)


import yaml
import json

from pathlib import Path

def load_cache_data(filepath: Path):
    with open(filepath, 'r') as file:
        return json.load(file)

def save_cache_data(filepath: Path, data):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w') as file:
        json.dump(data, file)

def load_config_file(path: Path) -> dict:
    with open(path) as file:
        content = file.read()
    res : dict = yaml.load(content, Loader=yaml.CLoader)
    return res

def load_playlist_file(path: Path, song_getter: Callable[str, Song]):
    with open(path, 'r') as file:
        data = file.read().strip().split('\n')
        for line in data:
            if line == '':
                continue
            song = song_getter(line)
            if song is not None:
                yield song

def save_playlist_file(path: Path, playlist_data: Iterable[str]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as file:
        for song_data in playlist_data:
            file.write(song_data)
            file.write('\n')

def scan_music_collection(path: Path, recurse: bool):
    cover = find_cover(path)
    newalbum = Album(path.stem, cover=cover)
    newalbum.extend(scan_album(newalbum, path, recurse))
    if len(newalbum) > 0:
        yield newalbum
    for file in path.iterdir():
        if file.is_dir():
            yield from scan_music_collection(file, recurse)

def is_music_file(path: Path) -> bool:
    return path.suffix in MUSIC_EXTENSIONS

def scan_album(album: Album, path: Path, recurse: bool):
    if recurse:
        iterator = path.rglob("*.*")
    else:
        iterator = path.glob("*.*")
    for file in iterator:
        if is_music_file(file):
            yield Song(file, album)

def find_cover(path: Path) -> Path | None:
    coverFile = None
    for file in path.glob("*.*"):
        if is_cover_file(file):
            if file.stem == MASTER_COVER_NAME:
                return file
            coverFile = file
    if coverFile is None:
        return FALLBACK_COVER
    return coverFile

def is_cover_file(path: Path) -> bool:
    return path.suffix in COVER_EXTENSIONS

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

import hashlib
import os
import subprocess
from pathlib import Path


BLOCK_SIZE = 32768

from maestro.utils.ressources import (
    USER_PLAYLIST_DIR,
)

def get_playlist_path(playlist_name: str) -> Path:
    if not playlist_name.endswith('.list'):
        playlist_name += '.list'
    path = Path(playlist_name)
    if path.is_absolute():
        return path
    return USER_PLAYLIST_DIR / path

def get_file_uid(path: Path) -> str:
    hobj = hashlib.sha1(usedforsecurity=False)
    with open(path, 'rb') as file:
        while True:
            data = file.read(BLOCK_SIZE)
            if data:
                hobj.update(data)
            else:
                break
    return hobj.hexdigest()

def fix_wm_class(class_name):
    pid = os.getpid()
    cmd = ["xdotool", "search", "--pid", str(pid)]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
    except FileNotFoundError:
        print("xdotool is not installed, cannot change wm_class")
        return
    winid = res.stdout.strip()
    cmd = [
        "xdotool",
        "set_window",
        "--class",
        class_name,
        "--classname",
        class_name,
        winid,
    ]
    subprocess.run(cmd)

def pager_print(text: str):
    pager = os.environ.get('PAGER', 'less')
    options = []
    if pager == 'less':
        options = ['--quit-if-one-screen', '--RAW-CONTROL-CHARS']
    try:
        subprocess.run([pager, *options], input=bytes(text, 'utf-8'))
    except KeyboardInterrupt:
        print()

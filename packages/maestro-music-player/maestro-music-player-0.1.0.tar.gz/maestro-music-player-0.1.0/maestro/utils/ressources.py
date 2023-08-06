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

import os

from pathlib import Path

ROOT = Path(__file__).parent.parent.parent

MEDIA = ROOT / "media"
FONTS = ROOT / "fonts"

# ---------------------------------- FILES ----------------------------------

# configuration files
DEFAULT_CONFIG_FILE = ROOT / "maestro/config_format.yaml"
TEST_CONFIG_FILE = ROOT / "maestro/maestro_test.yaml"
USER_CONFIG_FILE = Path("~/.config/maestro/maestro.yaml").expanduser()

# music collection
DEFAULT_COLLECTION_DIR = Path(os.environ.get('XDG_MUSIC_DIR') or "~/Music").expanduser()

# theme files
DEFAULT_THEME_FILE = ROOT / "maestro/theme_format.yaml"
THEME_DIRECTORY = ROOT / "maestro/themes"

# images
FALLBACK_COVER = MEDIA / "question.png"
DUMMY_COVER = MEDIA / "black.png"

# fonts
MONOSPACED_FONT = FONTS / 'Natural Mono-Regular.ttf'

# playlists
USER_PLAYLIST_DIR = Path("~/.config/maestro/playlists").expanduser()

# uid cache
UID_CACHE = Path("~/.cache/maestro/uids.json").expanduser()


# ------------------------------- FILE NAMES --------------------------------

MASTER_COVER_NAME = "cover"


# ----------------------------- FILE EXTENSIONS -----------------------------

MUSIC_EXTENSIONS = [".m4a", ".mp3", ".ogg", ".opus", ".wav"]

COVER_EXTENSIONS = [".jpg", ".jpeg", ".png"]

# --------------------------------- NAMES -----------------------------------

APP_NAME = "maestro"
DUMMY_NAME = "nothing to play"

EMPTY_ALBUM_NAME = "no album selected"

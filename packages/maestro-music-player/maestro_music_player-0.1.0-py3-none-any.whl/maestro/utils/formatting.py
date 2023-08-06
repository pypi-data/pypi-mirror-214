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

def format_time(total_ms: int) -> str:
    total_seconds = round(total_ms / 1000)
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02}:{seconds:02}"

def make_selection_tag(add_tag: bool) -> str:
    if add_tag:
        return f'•'
    else:
        return ' '

def with_selection_tag(text: str, add_tag: bool) -> str:
    if add_tag:
        tag = make_selection_tag(add_tag)
        return f'{tag} {text} {tag}'
    else:
        return text

def format_plural(count: int, singular: str, plural: str):
    if count == 1:
        return f'{count} {singular}'
    return f'{count} {plural}'

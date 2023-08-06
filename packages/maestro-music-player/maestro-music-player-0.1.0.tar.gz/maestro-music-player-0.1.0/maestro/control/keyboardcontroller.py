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

class KeyboardController:
    ALLOWED_MODIFIERS = set(['shift', 'ctrl', 'alt', 'meta'])

    def __init__(self, keymap: dict[str, callable]):
        self._keymap = keymap
        self.print_keycodes = False

    def keypress_event(self, keycode, modifiers):
        modifiers = list(set(modifiers) & self.ALLOWED_MODIFIERS)
        key_id, key_str = keycode
        key_names = []
        normal_key_name = "-".join([*modifiers, key_str])
        alt_key_name = "-".join([*modifiers, str(key_id)])
        if key_str == '':
            key_name_display = f'Key "{alt_key_name}"'
        else:
            key_name_display = f'Key "{normal_key_name}" or "{alt_key_name}"'
            key_names.append(normal_key_name)
        key_names.append(alt_key_name)
        command = None
        for key_name in key_names:
            try:
                command = self._keymap[key_name]
            except KeyError:
                pass
            else:
                break
        if command is None:
            if self.print_keycodes:
                return key_name_display
            return
        return command()

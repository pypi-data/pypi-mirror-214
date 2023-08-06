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
from maestro.view.termdocrender import TermDocRender
from maestro.systemutils.systemtools import pager_print


class DummyView:

    def launch_error(self, title: str, error_message: str, fatal: bool = False,
                     external_source: bool = False):
        print(f'{title}: {error_message}')

    def launch_info(self, message: str, external_source: bool = False):
        print(message)

    def show_doc_in_panel(self, doc):
        renderer = TermDocRender()
        doc.render(renderer)
        pager_print(renderer.result)

    def display_panel(self, *args, **kwargs):
        pass


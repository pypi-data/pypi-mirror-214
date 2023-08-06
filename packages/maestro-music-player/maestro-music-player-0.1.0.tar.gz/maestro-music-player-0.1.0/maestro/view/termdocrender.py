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
from maestro.model.documentation import (
    ContentPart,
)

import textwrap
import re

INDENT_WIDTH = 2

class TermColor:
    RED = '31m'
    GREEN = '32m'
    BLUE = '34m'
    CYAN = '36m'
    BOLD = '1m'

    @classmethod
    def style_text(cls, text: str, color: str):
        return f'\033[{color}{text}\033[0m'

class TermDocRender:

    def __init__(self, window_width: int = 90):
        self.window_width = window_width
        self._content = []
        self.line_buffer = []
        self.depth = 0
        self.headerMode = False
        self.tableMode = False
        self.margin = 0

    def render_content(self, content_item: ContentPart):
        lines = content_item.lines
        if self.tableMode:
            line = ' '.join(lines)
            if len(self.table_buffer) == 0:
                line = f'{line:20}'
            self.table_buffer.append(line)
            return
        style = content_item.style
        if style != 'codeblock':
            self.push_margin()
        for line in lines:
            if self.headerMode:
                line = TermColor.style_text(line, TermColor.BOLD)
            else:
                makebold = lambda m: TermColor.style_text(m.group(1), TermColor.BOLD)
                line = re.sub('`(.*?)`', makebold, line)
            self.push_content_line(line, style)
        if not (self.headerMode or style == 'codeblock'):
            self.push_margin()

    def push_content_line(self, line, style=None):
        if line.strip() == '' and style != 'codeblock':
            self.margin += line.count('\n') + 1
            lines = [line]
        else:
            self.margin = 0
            indent = ' '*self.depth*INDENT_WIDTH
            if style == 'codeblock':
                line = f'    {line}'
            lines = textwrap.wrap(line,
                                  width=self.window_width,
                                  initial_indent=indent,
                                  subsequent_indent=indent,
                                  replace_whitespace=False,
                                  drop_whitespace=True)
        self._content.extend(lines)

    def push_margin(self, size=1):
        missing_margin = max(size - self.margin, 0)
        if missing_margin > 0:
            self.push_content_line('\n'*(missing_margin-1))

    def start_section(self):
        self.depth += 1

    def end_section(self):
        self.depth -= 1

    def start_header(self):
        self.push_margin()
        self.headerMode = True

    def end_header(self):
        self.headerMode = False

    def start_table(self, columns):
        self.tableMode = True

    def end_table(self):
        self.tableMode = False

    def start_table_line(self):
        self.table_buffer = []

    def end_table_line(self):
        self.push_content_line(' '.join(self.table_buffer))

    @property
    def result(self):
        return '\n'.join(self._content).strip()

if __name__ == '__main__':
    from maestro.model.documentation import Text, Section, Table, TableLine
    doc = Section(Text('Top'),
                  Section(Text('ttt'), Section(Text('sub'), Table(TableLine(Text('what'))))),
                  Section(Section(Text('sub'), Table(TableLine(Text('what')))))
    )
    renderer = TermDocRender()
    doc.render(renderer)
    print(renderer.result)

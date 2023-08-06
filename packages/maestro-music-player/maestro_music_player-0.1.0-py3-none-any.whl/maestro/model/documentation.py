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

class DocPart:

    def render(self, render_engine): #pragma: no cover
        pass


class ContainerPart(DocPart):

    def __init__(self, *elements: DocPart):
        self.elements = list(elements)

    def add(self, element: DocPart):
        self.elements.append(element)

    def __getitem__(self, key):
        return self.elements[key]


class ContentPart(DocPart):
    pass


class Section(ContainerPart):

    def __init__(self, header: DocPart, *body: DocPart):
        self.header = header
        self.elements = list(body)

    def __eq__(self, other):
        return (isinstance(other, Section)
                and other.header == self.header
                and other.elements == self.elements)

    def render(self, render_engine):
        render_engine.start_header()
        self.header.render(render_engine)
        render_engine.end_header()
        render_engine.start_section()
        for elem in self.elements:
            elem.render(render_engine)
        render_engine.end_section()

    def __repr__(self):
        elems = ', '.join(repr(item) for item in [self.header, *self.elements])
        return f'Section({elems})'


class TableLine(ContainerPart):

    def render(self, render_engine):
        render_engine.start_table_line()
        for elem in self.elements:
            elem.render(render_engine)
        render_engine.end_table_line()

    def __eq__(self, other):
        return (isinstance(other, TableLine)
                and other.elements == self.elements)

    @property
    def columns(self):
        return len(self.elements)

    def __repr__(self):
        elems = '|'.join(repr(item) for item in self.elements)
        return f'TL[{elems}]'


class Table(ContainerPart):

    def __init__(self, *lines: TableLine, columns: int | None = None):
        self.elements = list(lines)
        if len(self.elements) > 0:
            self.columns = self.elements[0].columns
            if not all(elem.columns == self.columns for elem in self.elements):
                raise ValueError('All lines in the table should have the same number of columns')
            if columns is not None and columns != self.columns:
                raise ValueError('columns number should either be None or be consistent with the provided columns')
        else:
            if columns is None:
                raise ValueError('columns should be specified if no lines are provided')
            self.columns = columns

    def __eq__(self, other):
        return (isinstance(other, Table)
                and other.elements == self.elements)

    def add(self, line: TableLine):
        if line.columns != self.columns:
            raise ValueError(f'Lines in this table should have {self.columns} columns')
        self.elements.append(line)

    def render(self, render_engine):
        render_engine.start_table(columns=self.columns)
        for line in self.elements:
            line.render(render_engine)
        render_engine.end_table()

    def __repr__(self):
        elems = ', '.join(repr(item) for item in self.elements)
        return f'Table({elems})'


class Text(ContentPart):

    def __init__(self, *content: str, link=None, style=None):
        self.lines = list(content)
        self.link = link
        self.style = style

    def __eq__(self, other):
        return (isinstance(other, Text)
                and other.lines == self.lines)

    def render(self, render_engine):
        render_engine.render_content(self)

    def __repr__(self):
        text = ' '.join(self.lines)
        return f'T"{text}"'

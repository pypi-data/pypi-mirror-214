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
from typing import Tuple

from maestro.model.documentation import (
    DocPart,
    Text,
    Section,
)

import re
import textwrap

BIG_ENOUGH = 100000

def extract_index(name: str) -> Tuple[int, str]:
    patterns = [
        # a number at the begining
        # '123 The Title - The Artist' ----> 123
        r"(^)(\d+)([.)]?\s*-?\s*\W)",
        # a number somewhere in the middle followed by a dot
        # 'Album 2 - 05. Awesome - The Artist' ----> 5
        r"(\s*\W)(\d+)([.]\s*-?\s*\W)",
        # a number somewhere in the middle followed by a dot
        # 'My music - 34 carrot cake ----> 34
        r"(\s*\W)(\d+)(\s*-?\s*\W)",
    ]
    for pattern in patterns:
        result = re.search(pattern, name)
        if result is not None:
            break
    if result is None:
        return BIG_ENOUGH, name
    number = result.group(2)
    new_name = name.replace(result.group(0), " ").strip()
    return int(number), new_name

def parse_color(color_str: str) -> Tuple[float, ...]:
    error = ValueError(f'Invalid color string {color_str}')
    if len(color_str) != 7 or color_str[0] != '#':
        raise error
    try:
        color = tuple(int(color_str[i:i+2], 16) / 255 for i in range(1, 7, 2))
    except ValueError as e:
        raise error
    return color

def make_paragraphs(text: str) -> list[str]:
    parts = text.strip().split('\n\n')
    paragraphs = [
        ' '.join(line.strip() for line in part.split('\n'))
        for part in parts
    ]
    return paragraphs

def make_description(description: str | None) -> (str, list[str]):
    if description is None:
        return '', []
    summary, *description = make_paragraphs(description)
    assert '\n' not in summary, description
    return summary, description


class MDDocPageBuilder:

    def __init__(self, text: str):
        self.paragraph_buffer = []
        self.heading_level = 0
        self.doc_stack = []
        self.current_section = None
        self.code_block_mode = False
        dedented_text = textwrap.dedent(text)
        self.tokens = dedented_text.strip().split('\n')

    def render_as_documentation(self):
        for token in self.tokens:
            self.process_token(token)
        self.push_paragraph()
        for i in range(self.heading_level - 1):
            self.close_heading()
        return self.current_section

    def open_heading(self, heading_name: str):
        new_section = Section(Text(heading_name))
        if self.current_section is not None:
            self.current_section.add(new_section)
            self.doc_stack.append(self.current_section)
        self.current_section = new_section
        self.heading_level += 1

    def close_heading(self):
        self.heading_level -= 1
        if self.doc_stack == []:
            raise ValueError('Broken heading hierarchy')
        else:
            self.current_section = self.doc_stack.pop()

    def push_paragraph(self):
        if self.paragraph_buffer == []:
            return
        if self.current_section is None:
            raise ValueError('Expecting a section start before paragraph')
        if self.code_block_mode:
            text = Text(*self.paragraph_buffer, style='codeblock')
        else:
            text = Text(' '.join(self.paragraph_buffer))
        self.paragraph_buffer = []
        self.current_section.add(text)

    def process_token(self, token):
        if token.startswith('```'):
            self.push_paragraph()
            self.code_block_mode = not self.code_block_mode
        elif self.code_block_mode:
            self.paragraph_buffer.append(token)
        elif token == '':
            self.push_paragraph()
        elif token.startswith('-'):
            self.push_paragraph()
            self.paragraph_buffer.append(token)
        elif token.startswith('#'):
            self.push_paragraph()
            heading_tag, heading_name = token.split(' ', 1)
            level = len(heading_tag)
            if level <= self.heading_level:
                for i in range(self.heading_level - level + 1):
                    self.close_heading()
            self.open_heading(heading_name)
        else:
            self.paragraph_buffer.append(token)


def make_doc_page(text: str) -> DocPart:
    '''
    Convert a markdown-like string into a documentation page

    Supported syntax:
        - '#' for section headings
        - blank line to separate paragraphs
    '''
    builder = MDDocPageBuilder(text)
    return builder.render_as_documentation()

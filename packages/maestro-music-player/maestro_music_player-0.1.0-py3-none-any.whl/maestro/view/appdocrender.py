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
from kivy.factory import Factory
from kivy.lang import Builder

import re

from maestro.model.documentation import (
    ContentPart,
)

MAX_FONT_SIZE = 30
MIN_FONT_SIZE = 16

class AppDocRender:

    def __init__(self):
        self.widget_stack = []
        self.root_widget = Factory.DocRoot()
        self.container = self.root_widget
        self.depth = 0
        self.headerMode = False
        self.tableMode = False
        self.margin = 0

    def render_content(self, content_item: ContentPart):
        text = '\n'.join(content_item.lines)
        makebold = lambda m: f'[b]{m.group(1)}[/b]'
        text = re.sub('`(.*?)`', makebold, text)
        if self.tableMode:
            width = 0.2 if self.line_index == 0 else 0.8
            label = Factory.DocTableLabel(text=text,
                                          depth=self.depth,
                                          font_size=MIN_FONT_SIZE,
                                          size_hint_x=width,
            )
            self.line_index += 1
        elif self.headerMode:
            font_size = (MAX_FONT_SIZE - MIN_FONT_SIZE)*0.4**self.depth + MIN_FONT_SIZE
            text = f'[b]{text}[/b]'
            label = Factory.DocHeaderLabel(text=text, depth=self.depth,
                                           font_size=font_size)
        else:
            options = {}
            if content_item.style == 'codeblock':
                constructor = Factory.DocCodeblockLabel
            else:
                constructor = Factory.DocLabel
            label = constructor(text=text, depth=self.depth,
                                font_size=MIN_FONT_SIZE)
        if self.container is None:
            raise Exception('Invalid documentation tree, cannot have ContentPart as root')
        else:
            self.container.add_widget(label)

    def add_new_container(self, widget):
        if self.container is None:
            raise Exception('Invalid documentation tree')
        else:
            self.container.add_widget(widget)
            self.widget_stack.append(self.container)
        self.container = widget

    def close_current_container(self):
        self.container = self.widget_stack.pop() if self.widget_stack else None

    def start_section(self):
        self.depth += 1
        box = Factory.DocSectionBody(depth=self.depth)
        self.add_new_container(box)

    def end_section(self):
        self.close_current_container()
        self.close_current_container()
        self.depth -= 1

    def start_header(self):
        box = Factory.DocSection(depth=self.depth)
        self.add_new_container(box)
        self.headerMode = True

    def end_header(self):
        self.headerMode = False

    def start_table(self, columns):
        self.tableMode = True
        self.line_count = 0
        box = Factory.DocTable(depth=self.depth)
        self.add_new_container(box)

    def end_table(self):
        self.tableMode = False
        self.close_current_container()

    def start_table_line(self):
        self.line_index = 0
        alt = self.line_count % 2
        box = Factory.DocTableLine(orientation='horizontal', alt=alt)
        self.add_new_container(box)
        self.line_count += 1

    def end_table_line(self):
        self.close_current_container()
        pass

    @property
    def result(self):
        return self.root_widget


if __name__ == '__main__':
    from kivy.app import App
    from maestro.control.configmanager import ConfigManager
    from maestro.utils.ressources import (
        DEFAULT_CONFIG_FILE,
    )
    from maestro.utils.loaders import (
            load_config_file,
    )
    from maestro.model.documentation import (
        Section,
        Text,
        Table,
        TableLine,
    )
    import panels


    class DemoApp(App):

        def build(self):
            specifications = load_config_file(DEFAULT_CONFIG_FILE)
            self.config = ConfigManager(specifications)
            doc = Section(Text('Hello'),
                          Text('This is some text\nwith multiple lines'),
                          Text('This is some text\nwith multiple lines'),
                          Section(Text('Part 1'),
                                  Text('A nested section'),
                                  Text('with other informations'),
                          ),
                          Section(Text('Part 2'),
                                  Text('Another section with a bit more information'),
                                  Text('we are testing the in-app documentation rendering engine to see if everything works as expected and is integrated properly. We aim for the best quality and intuitive user interface. I don’t know what to write but I just need some text to test this documentation display so I write any text in english as long as it looks like real text, it gets the job done. I should probably stop now and implement the real thing.'),
                          ),
                          Section(Text('Part 3'),
                                  Table(TableLine(Text('one'), Text('item')),
                                        TableLine(Text('two'), Text('items')),
                                        TableLine(Text('a quite long one'), Text('with text')),
                                        TableLine(Text('and'), Text('some asymetry in length')),
                                        TableLine(Text('last'), Text('an overly way to long and to bigto long and to big to long and to big to long and to big to long and to big text\nwith even multiple lines')),
                                  )
                          )
            )
            Builder.load_file('panel_common.kv')
            Builder.load_file('doc_panel.kv')
            renderer = AppDocRender()
            doc.render(renderer)
            sm = Factory.ScreenManager()
            panel = Factory.DocPanel()
            panel.scroll_view.add_widget(renderer.result)
            sm.add_widget(panel)
            return sm

        def get_theme_color(self, theme_field):
            config_field = f"theme.{theme_field}"
            color = self.config.ask_key(config_field)
            return color


    app = DemoApp()
    app.run()



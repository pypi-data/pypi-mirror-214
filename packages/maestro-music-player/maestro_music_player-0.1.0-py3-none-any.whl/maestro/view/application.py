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

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import (
    StringProperty,
    BooleanProperty,
    NumericProperty,
)

from maestro.systemutils.systemtools import fix_wm_class

from maestro.view.constants import (
    PING_REFRESH_RATE,
    APP_TITLE,
    APP_ICON,
    RESEND_KEY_DELAY,
)
import maestro.view.panels


class MaestroApp(App):
    loop = BooleanProperty()
    current_song_cover = StringProperty()
    current_song_name = StringProperty()
    current_album_name = StringProperty()
    current_song_time = NumericProperty(0)
    current_song_duration = NumericProperty(0)
    volume_level = NumericProperty(100)
    queue_status = StringProperty()

    def __init__(self, thememanager):
        super().__init__(title=APP_TITLE, icon=APP_ICON)
        # fix class name
        fix_wm_class("maestro")
        # keyboard setup
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self.root, "text"
        )
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        self.window_focused = True
        self.ignore_next_enter = False
        self.thememanager = thememanager
        # error management
        self.message_popup: None | Popup = None
        self.fatal_error: bool = False
        Clock.max_iteration = 30 # this is to suppress a kivy warning

    async def async_run(self):
        await super().async_run(async_lib='trio')

    @property
    def current_panel_columns(self):
        return self.root.panel_manager.current_screen.columns

    def register_controller(self, controller):
        self.controller = controller

    def get_theme_color(self, theme_field):
        config_field = f"theme.{theme_field}"
        color = self.thememanager.ask_key(config_field)
        return color

    def get_panel_item_color(self, field: str, focused: bool, alt: bool,
                             playing=False):
        match (focused, playing):
            case (True, True):
                color_name = 'focused_playing'
            case (True, False):
                color_name = 'focused'
            case (False, True):
                color_name = 'playing'
            case (False, False):
                color_name = 'normal'
            case _:
                color_name = 'normal'
        alt_tag = '_alt' if alt else ''
        key = f'panel_items.{color_name}{alt_tag}.{field}'
        return self.get_theme_color(key)

    def update_panel(self, panel_name: str, panel_data):
        screen = self.root.panel_manager.get_screen(panel_name)
        screen.set_data(panel_data)

    def update_queue_status(self, playing_index, queue_length):
        index = "-" if playing_index is None else f"{playing_index+1}"
        self.queue_status = f"{index} / {queue_length}"

    def display_panel(self, panel_name: str):
        self.root.panel_manager.current = panel_name

    def launch_error(self, title: str, error_message: str, fatal: bool = False,
                     external_source: bool = False):
        if external_source:
            return f'{title}: {error_message}'
        self.message_popup = Popup(
            title=title,
            content=Label(text=error_message),
            size_hint=(1, None),
            height=200,
        )
        self.fatal_error = fatal
        self.message_popup.open()

    def launch_info(self, message: str,
                    external_source: bool = False):
        if external_source:
            return message
        if self.message_popup is not None:
            self.dismiss_popup()
        self.message_popup = Popup(
            title="Info",
            content=Label(text=message,
                          halign='left'),
            size_hint=(1, 1),
        )
        self.message_popup.open()

    def show_doc_in_panel(self, doc):
        self.root.doc_panel.render_doc(doc)

    def dismiss_popup(self):
        if self.message_popup is not None:
            self.message_popup.dismiss()
            self.message_popup = None
            if self.fatal_error:
                self.stop()

    def set_playing_song(self, name: str, cover: str, album: str):
        self.current_song_name = name
        self.current_song_cover = cover
        self.current_album_name = album

    def set_playing_progress(self, time, duration):
        self.current_song_time = time
        self.current_song_duration = duration

    def set_loop_status(self, loop: bool):
        self.loop = loop

    def set_volume_level(self, volume: int):
        self.volume_level = volume

    def _keyboard_closed(self):
        pass

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if self.ignore_next_enter:
            return True
        if not self.window_focused:
            return True
        self.controller.keypress_event(keycode, modifiers)
        # Return True to accept the key. Otherwise, it will be used by the system.
        return True

    def _on_keyboard_up(self, keyboard, keycode):
        if self.ignore_next_enter:
            self.ignore_next_enter = False
            return True
        return True

    def on_focus(self, window, focus):
        if focus:
            Clock.schedule_once(self.reactivate_window_focus, RESEND_KEY_DELAY)
        else:
            self.window_focused = False

    def reactivate_window_focus(self, *args):
        self.window_focused = True

    def command_line(self, focus: bool, text=None):
        self.root.command_bar.focus = focus
        if text is not None:
            self.root.command_bar.text = text

    def on_command_mode(self, textinput, focused):
        self.controller.command_line_focus_event(focused)

    def execute_command(self, command_line: str):
        if command_line.strip() != '':
            self.controller.command_line_event(command_line,
                                               external_source=False)
        self.root.command_bar.text = ""
        # This hack is necessary because when we hit enter in the in-app
        # command line, the enter key is still send to _on_keyboard_down
        # so we must ignore it
        self.ignore_next_enter = True

    def on_start(self):
        self.controller.app_start_event()
        self.root.command_bar.bind(focus=self.on_command_mode)
        self.root_window.bind(focus=self.on_focus)
        Clock.schedule_interval(self.ping_refresh, PING_REFRESH_RATE)

    def ping_refresh(self, time):
        self.controller.ping_refresh()

    def on_stop(self):
        self.controller.close_app_event()

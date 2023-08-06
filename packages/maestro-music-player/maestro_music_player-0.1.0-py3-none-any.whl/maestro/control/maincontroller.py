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

from maestro.control.keyboardcontroller import KeyboardController
from maestro.control.configmanager import ConfigManager, InvalidConfig
from maestro.control.commandmanager import (
    CommandInterface,
    CommandGroup,
    ThematicGroup,
    CommandError,
    command,
    flag_arg,
    int_arg,
    bool_arg,
    str_arg,
    greedy_str_arg,
)

from maestro.model.collection import MusicCollection, Song, ComputationNotReady
from maestro.model.application import AppMode
from maestro.model.documentation import (
    DocPart,
    Section,
    Text,
)
from maestro.utils.parsing import make_doc_page


from maestro.utils.loaders import (
        load_config_file,
        load_cache_data,
        save_cache_data,
        load_playlist_file,
        save_playlist_file,
        scan_music_collection,
)
from maestro.systemutils.systemtools import get_playlist_path

from maestro.utils.ressources import (
    DEFAULT_CONFIG_FILE,
    DEFAULT_THEME_FILE,
    DEFAULT_COLLECTION_DIR,
    THEME_DIRECTORY,
    USER_CONFIG_FILE,
    UID_CACHE,
    APP_NAME,
    USER_PLAYLIST_DIR,
)

from pathlib import Path

import trio


class MainController(CommandInterface):

    @classmethod
    def dummy(cls):
        return cls(_dummy=True)

    def __init__(self, *args, _dummy=False, **kwargs):
        super().__init__(APP_NAME)
        config_specs = load_config_file(DEFAULT_CONFIG_FILE)
        self.configmanager = ConfigManager(config_specs)
        theme_specs = load_config_file(DEFAULT_THEME_FILE)
        self.thememanager = ConfigManager(theme_specs)
        if _dummy:
            from maestro.view.dummyview import DummyView
            self.view = DummyView()
        else:
            self._init(*args, **kwargs)

    def _init(self, model, view, sound, user_config: Path,
                 cache_file: Path = UID_CACHE):
        self.model = model()
        self.sound_class = sound
        self.cache_file = cache_file
        self.load_user_config(user_config)
        self.view = view(self.thememanager)
        self.view.register_controller(self)
        self.keyboard_controllers = {}
        self.song_player = None
        self.collection_scan_success = False
        self.initialization_done = trio.Event()
        self.uids_computed = trio.Event()

    # runner
    async def async_run(self): # pragma: no cover
        async with trio.open_nursery() as nursery:
            nursery.start_soon(self.view.async_run)
            nursery.start_soon(self.compute_song_uids)

    # Events -----------------------------------------------------------------

    def keypress_event(self, *args, **kwargs):
        controller = self.keyboard_controllers.get(self.model.mode)
        if controller:
            result = controller.keypress_event(*args, **kwargs)
            self.handle_command_result(result, external_source=False)

    def command_line_focus_event(self, command_line_focused: bool):
        if command_line_focused and self.model.mode == AppMode.NORMAL:
            self.model.switch_to_mode(AppMode.COMMAND)
        elif not command_line_focused and self.model.mode == AppMode.COMMAND:
            self.model.switch_to_mode(AppMode.NORMAL)

    def handle_command_result(self, result, external_source: bool):
        if result is not None:
            if isinstance(result, DocPart):
                self.view.show_doc_in_panel(result)
                self.view.display_panel('documentation')
            else:
                if not external_source:
                    self.model.switch_to_mode(AppMode.POPUP)
                return self.view.launch_info(result,
                                             external_source=external_source)

    def command_line_event(self, command: str, external_source=True):
        try:
            result = self.interprete_command(command)
        except CommandError as error:
            message = str(error)
            if not external_source:
                self.model.switch_to_mode(AppMode.POPUP)
            return self.view.launch_error("Invalid command", message,
                                          external_source=external_source)
        return self.handle_command_result(result, external_source)

    def load_user_config(self, user_config_file: Path):
        # load config
        self.config_error = None
        try:
            user_config = load_config_file(user_config_file)
            self.configmanager.set_user_config(user_config)
        except FileNotFoundError:
            self.config_error = (
                'No configuration file found\n'
                'Create a configuration file to start using maestro\n'
                'See "help setup" for more details'
            )
        except InvalidConfig as error:
            self.config_error = str(error)
        # load theme
        user_theme_name = self.configmanager.ask_key('theme.name')
        user_theme_file = f'{user_theme_name}.yaml'
        fallback_theme_name = self.configmanager.ask_key('theme.name',
                                                         force_default=True)
        fallback_theme_file = f'{fallback_theme_name}.yaml'
        theme_paths = (
            user_config_file.parent / 'themes' / user_theme_file,
            THEME_DIRECTORY / user_theme_file,
        )
        self.theme_error = None
        for theme_path in theme_paths:
            self.theme_error = self._load_theme_file(theme_path)
            if self.theme_error is None:
                return
        self._load_theme_file(THEME_DIRECTORY / fallback_theme_file)

    def _load_theme_file(self, theme_path: Path):
        try:
            theme = load_config_file(theme_path)
            self.thememanager.set_user_config(theme)
        except FileNotFoundError:
            return f'Theme {theme_path} not found'
        except InvalidConfig as error:
            return str(error)

    def _app_start_event(self):
        # load config
        if self.config_error is not None:
            self.model.switch_to_mode(AppMode.POPUP)
            self.view.launch_error("Invalid config", self.config_error, fatal=True)
            return
        if self.theme_error is not None:
            self.model.switch_to_mode(AppMode.POPUP)
            self.view.launch_error("Invalid theme", self.theme_error)
        # setup keyboard mapping
        self.keyboard_controllers = {}
        for mode in AppMode:
            config_key = f'keys.{mode.name.lower()}'
            raw_keymap = self.configmanager.ask_key(config_key)
            try:
                controller = KeyboardController(
                    {key: self.prepare_command(cmd)
                     for key, cmd in raw_keymap.items()}
                )
            except CommandError as error:
                message = (f"{str(error)}\n"
                           f"Fix the invalid config and restart maestro")
                self.model.switch_to_mode(AppMode.POPUP)
                self.view.launch_error("Invalid config", message, fatal=True)
                return
            else:
                self.keyboard_controllers[mode] = controller
        # setup audio backend
        audio_backend = self.configmanager.ask_key('audio.backend')
        try:
            self.song_player = self.sound_class(audio_backend)
        except ValueError:
            message = f'Unsupported audio.backend "{audio_backend}"'
            self.model.switch_to_mode(AppMode.POPUP)
            self.view.launch_error("Invalid config", message, fatal=True)
            return
        # load song uid cache
        try:
            cache = load_cache_data(self.cache_file)
            self.model.load_songuid_cache(cache)
        except FileNotFoundError:
            pass
        # scan music collection
        self.scan_collection()
        # set loop status
        self.view.set_loop_status(self.model.loop)
        # set volume level
        volume = max(self.song_player.volume, 0)
        self.view.set_volume_level(volume)
        # init doc panel
        doc = self.interprete_command('help')
        self.view.show_doc_in_panel(doc)

    def app_start_event(self):
        res = self._app_start_event()
        self.initialization_done.set()
        return res

    async def compute_song_uids(self):
        await self.initialization_done.wait()
        await self.model.collection.build_song_table()
        self.uids_computed.set()

    def close_app_event(self):
        if self.collection_scan_success and self.model.songcache_was_modified:
            cache = self.model.get_songuid_cache()
            save_cache_data(self.cache_file, cache)

    def ping_refresh(self):
        if self.song_player is None:
            return
        self.song_player.ping()
        time = max(self.song_player.time, 0)
        duration = max(self.song_player.duration, 0)
        self.view.set_playing_progress(time, duration)
        if self.song_player.is_idle and not self.model.playing_song.is_dummy:
            self.play_next()

    # Commands ---------------------------------------------------------------

    with ThematicGroup("Interface"):

        @command(
            "show-panel",
            flag_arg("collection", "album", "queue", "documentation", name='<panel>'),
            description='Show a specific panel',
        )
        def show_panel(self, panel_name: str):
            self.model.show_panel(panel_name)
            self.view.update_panel(panel_name,
                                   self.model.current_panel)
            self.view.display_panel(panel_name)

        with CommandGroup("focus", description='Move the focus around'):

            @command("move", flag_arg("up", "down", "left", "right",
                                      name='<direction>'),
                     description='''
            Focus a nearby element in the central panel

            Note: `left` and `right` only have an effect in the collection panel
            ''')
            def move_focus(self, direction: str):
                cols = self.view.current_panel_columns
                increment = {"up": -cols, "down": cols, "left": -1, "right": 1}
                self.model.move_focus(increment[direction])
                self.show_current_panel()

            @command("set", flag_arg('top', 'bottom', 'playing',
                                     name='<location>'),
                     description='''
            Jump to a specific element in the central panel

            Note: `playing` has an effect only in the queue panel
            ''')
            def set_focus(self, focus_value: str):
                panel_length = len(self.model.current_panel)
                if panel_length == 0:
                    return
                match focus_value:
                    case 'top':
                        self.model.focused_index = 0
                    case 'bottom':
                        self.model.focused_index = panel_length - 1
                    case 'playing' if self.model.current_panel.name == 'queue':
                        if self.model.playing_index is not None:
                            self.model.focused_index = self.model.playing_index
                self.show_current_panel()


        @command("select",
                 flag_arg('all', 'current', name='<range>'),
                 description='''
        Add items to the selection
        ''')
        def select(self, selection: str):
            match selection:
                case 'current':
                    self.model.current_panel.select_focused(select=True)
                case 'all':
                    self.model.current_panel.select_all(select=True)
            self.show_current_panel()

        @command("deselect",
                 flag_arg('all', 'current', name='<range>'),
                 description='''
        Remove items from the selection
        ''')
        def deselect(self, selection: str):
            match selection:
                case 'current':
                    self.model.current_panel.select_focused(select=False)
                case 'all':
                    self.model.current_panel.select_all(select=False)
            self.show_current_panel()

        @command("toggle-select",
                 flag_arg('all', 'current', name='<range>'),
                 description='''
        Toggle the selection state of items
        ''')
        def toggle_select(self, selection: str):
            match selection:
                case 'current':
                    self.model.current_panel.select_focused(invert=True)
                case 'all':
                    self.model.current_panel.select_all(invert=True)
            self.show_current_panel()

    with ThematicGroup("Actions"):

        with CommandGroup("current",
                          description='Action on the currently focused element'):

            @command('show', description='Show the album of the focused element')
            def current_show(self):
                match self.model.current_panel.name:
                    case 'collection':
                        album = self.model.focused_item
                    case 'album':
                        return
                    case 'documentation':
                        return
                    case _:
                        album = self.model.focused_item.album
                self.model.show_album_in_album_panel(album)
                self.show_panel('album')

            @command('add', description='Add the focused element to queue')
            def current_add(self):
                if self.model.current_panel.name == 'documentation': return
                self.model.add_focused_to_queue()
                self.show_queue_status()
                self.show_current_panel()

            @command('play', description='''
            Play this song now

            The player will jump to the focused song and start to play it
            This command works only in the queue panel'''
            )
            def current_play(self):
                if self.model.current_panel.name != 'queue':
                    return
                self.model.playing_index = self.model.focused_index
                self.start_playing_song()

            @command('remove', description='''
            Remove this song from the queue

            The song under focus is removed from the queue.
            If that song was currently playing, the player stops
            This command works only in the queue panel'''
            )
            def current_remove(self):
                if self.model.current_panel.name != 'queue':
                    return
                if self.model.focused_index == self.model.playing_index:
                    self.stop_playing()
                self.model.current_panel.delete_focused()
                self.show_queue_status()
                self.show_current_panel()

        with CommandGroup("selection", description='Action on the selection'):

            @command("add", description='''
            Add selected elements to the queue
            ''')
            def add_selection(self):
                if self.model.current_panel.name == 'documentation': return
                self.model.add_selection_to_queue()
                self.show_queue_status()
                self.show_current_panel()

            @command("remove", description='''
            Remove selected elements from the queue

            This command only works in the queue panel
            ''')
            def remove_selection(self):
                if self.model.current_panel.name != 'queue':
                    return
                if self.model.current_panel.is_selected(self.model.playing_index):
                    self.stop_playing()
                self.model.current_panel.delete_selected()
                self.show_queue_status()
                self.show_current_panel()

        with CommandGroup("queue", description='Action on the queue'):

            @command("clear", description='Clear the queue and stop playing')
            def queue_clear(self):
                self.model.clear_queue()
                self.song_player.stop()
                self.show_playing_song(Song.dummy())
                self.show_current_panel()

            @command("shuffle", description='''
            Shuffle the queue

            Note: this also stops playing the queue
             ''')
            def queue_shuffle(self):
                self.model.shuffle_queue()
                self.song_player.stop()
                self.show_playing_song(Song.dummy())
                self.show_current_panel()


        with CommandGroup("playlist", description="Manage playlists"):

            @command("save", str_arg('filename or path of the playlist to save',
                                     name='<filename>'),
                     description=f'''
            Save the queue as a playlist

            If only a filename is provided, the playlist will be saved to the
            user playlist directory, which by default is {USER_PLAYLIST_DIR.as_posix()}
            ''')
            def save_playlist(self, filepath: str):
                destination_path = get_playlist_path(filepath)
                playlist_data = self.model.queue_playlist_data
                save_playlist_file(destination_path, playlist_data)

            @command("load", str_arg('filename or path of the playlist to load',
                                     name='<filename>'),
                     description=f'''
            Load a playlist to the queue

            The playlist content is appended to the queue

            If only a filename is provided, the playlist will be loaded from the
            user playlist directory, which by default is {USER_PLAYLIST_DIR.as_posix()}
            ''')
            def load_playlist(self, filepath: str):
                source_path = get_playlist_path(filepath)
                try:
                    iter_songs = load_playlist_file(source_path,
                                                    self.model.song_getter)
                    self.model.add_playlist_to_queue(iter_songs)
                except FileNotFoundError:
                    raise CommandError(f'Playlist "{filepath}" could not be found')
                except ComputationNotReady as error:
                    raise CommandError(
                        f'Maestro is still scanning and indexing your music collection\n'
                        f'Loading playlists will be possible once this task is done.\n'
                        f'Indexing progress: {error}'
                    )
                self.show_queue_status()
                self.show_current_panel()

    with ThematicGroup("Player"):

        @command("play", description='''
        Start playing music

        If the queue is not playing, the queue will start to play from the beginning
        ''')
        def play(self):
            if self.song_player.is_idle:
                self.play_next()
            else:
                self.song_player.play()

        @command("pause", description='''
        Pause the music

        Use `play` or `play-pause` to resume'''
        )
        def pause(self):
            self.song_player.pause()

        @command("play-pause", description='''
        Toggle between play and pause

        If the queue is not playing, the queue will start to play from the beginning
        ''')
        def play_pause(self):
            if self.song_player.is_idle:
                self.play()
            else:
                self.song_player.toggle_play_pause()

        @command("next", description='''
        Play the next song

        If the player is stopped, start to play the queue from the beginning
        ''')
        def play_next(self):
            self.model.play_next()
            self.start_playing_song()

        @command("previous", description='''
        Play the previous song

        If the player is stopped, start to play the queue from the end
        ''')
        def play_previous(self):
            self.model.play_previous()
            self.start_playing_song()

        @command("stop", description='''
        Stop playing the queue

        When the player starts playing again, the queue will start from the beginning
        ''')
        def stop_playing(self):
            self.model.stop_playing()
            self.song_player.stop()
            self.show_playing_song(Song.dummy())
            self.show_current_panel()

        @command("loop", bool_arg(name='<status>'),
                 description='''
        Control whether the queue loops

        If on, the queue starts playing again from the beginning when it reaches the end.
        If off, the queue stops playing when it reaches the end.
        ''')
        def set_loop(self, status: bool):
            self.model.loop = status
            self.view.set_loop_status(status)

        @command(
            "volume",
            flag_arg("set", "increment", "decrement", name='<action>'),
            int_arg(),
            description='Control the audio volume'
        )
        def volume(self, action: str, value_str: str):
            value = int(value_str)
            match action:
                case "set":
                    self.song_player.set_volume(value)
                case "increment":
                    self.song_player.increment_volume(value)
                case "decrement":
                    self.song_player.increment_volume(-value)
            self.song_player.ping()
            volume = max(self.song_player.volume, 0)
            self.view.set_volume_level(volume)


    with ThematicGroup("Interface utils"):

        @command("command-line",
                 flag_arg("focus", "leave", "clear", name='<action>'),
                 description='''
        Action on the in-app command line

        `focus` will focus the command line, allowing to type a command
        `leave` will unfocus the command line
        `clear` will unfocus the command line and clear the text typed in it

        This command is obviously useless to use on the command line and is meant
        to be bound to a key in the config file
        ''')
        def command_line(self, action: str):
            match action:
                case 'focus':
                    self.view.command_line(focus=True)
                case 'leave':
                    self.view.command_line(focus=False)
                case 'clear':
                    self.view.command_line(focus=False, text="")

        @command("dismiss-popup",
                 description='''
        Dismiss an error message popup

        This command is meant to be bound to a key in the config file,
        as typing commands is disabled while there is a popup.
        When binding `dismiss-popup`, make sure to bind it for "popup" mode,
        otherwise it will have no effect.
        ''')
        def dismiss_popup(self):
            # do not print keycodes once the popup is dismissed
            controller = self.keyboard_controllers[AppMode.POPUP]
            controller.print_keycodes = False
            # dismiss the popup
            if self.model.mode == AppMode.POPUP:
                self.model.switch_to_mode(AppMode.NORMAL)
                self.view.dismiss_popup()

        @command("print-keycodes",
                 description='''
        Print the key codes

        Use this to find out the name of a key to bind a command to it.
        ''')
        def print_keycodes(self):
            controller = self.keyboard_controllers[AppMode.POPUP]
            controller.print_keycodes = True
            self.model.switch_to_mode(AppMode.POPUP)
            self.view.launch_info('Press any key…', external_source=False)

    with ThematicGroup("External commands"):

        @command("get",
                 flag_arg('playing-title', name='<key>'),
                 description='''
        Get some information about the application

        This command allows an external program to get information about a running
        maestro instance. For instance, this command could be used to display
        the name of the currently playing song in the status bar of your desktop
        environment.
        ''')
        def get_information(self, information: str):
            return self.model.playing_song.name

    with ThematicGroup("Various"):

        with CommandGroup("help", description='Show help about various aspects of maestro',
                          fallback_path='iamlost'):


            @command("setup", description='How to setup maestro')
            def setup_help(self):
                return make_doc_page(
            f'''
            # Initial setup

            Before using maestro, you need to setup a few things in it’s
            configuration file, which for you is located at `{USER_CONFIG_FILE}`

            ## Music collection

            The first thing to setup is the key `music_collection`, which
            specifies in which directory maestro should look for music files.

            Example:
            ```
            # maestro.yaml

            music_collection: "~/Music"
            ```

            ## Setup an audio backend

            Maestro is using mpv under the hood to play your music. You should
            have mpv installed on your system for maestro to work.
            Alternatively, vlc can be used instead. In that case, you should
            specify it in the configuration file by setting `audio.backend`

            Example:
            ```
            # maestro.yaml

            audio:
                backend: 'vlc'
            ```

            ## Add some keybindings

            In maestro, all interactions with the application are done through
            commands. You can invoke commands from the command line or you can
            bind them to a key in your configuration file.

            By default, maestro has no keybindings, to avoid surprising you with
            unexpected behaviours.

            Here is an example possible configuration:

            ```
            # maestro.yaml

            keys:
              normal:
                'left': 'focus move left'
                'right': 'focus move right'
                'up': 'focus move up'
                'down': 'focus move down'

                'enter': 'current show'
                'a': 'current add'
                'delete': 'current remove'

                '1': 'show-panel collection'
                '2': 'show-panel album'
                '3': 'show-panel queue'
                '4': 'show-panel documentation'

                '+': 'volume increment 5'
                '-': 'volume decrement 5'

                'spacebar': 'play-pause'
                'p': 'previous'
                'n': 'next'

            popup:
              'escape': 'dismiss-popup'
            ```

            That’s all you need to get started.
            You can now launch the application and starting playing some music.
            Later on, you can add more keybindings and tweak more options.

            If you are new to maestro, have a look at `help tutorial`
            ''')

            @command("tutorial", description='Discover the main features of maestro')
            def tutorial_help(self):
                return make_doc_page(
            '''
            # Welcome tutorial

            This tutorial will help you to get started with maestro.

            Make sure you have followed the setup tutorial first.
            If not, see `help setup`

            ## Interface overview

            Maestro is composed of a status bar at the top (which shows
            various informations like the current song playing…),
            a central area and a command line at the bottom.

            The central area can display different panels:
            - the collection panel, which shows all your albums
            - the album panel, which shows the songs in a given album
            - the queue panel, which shows the queued song waiting to be played
            - the documentation panel, which shows the documentation

            ## Music tree

            Maestro will scan your `music_collection` directory and look for 
            audio files. Each audio file will become a song and each directory
            will become an album. The file/directory name will be the song/album
            name. If there is a picture file in an album directory, it will be
            used as the album cover.

            As you see, maestro relies on your directory structure to determine
            albums and songs. That way, you can easily arrange your albums as
            you wish from your file manager and the changes will be reflected
            in maestro. No need for special tools to edit metadata.

            ## Commands

            Maestro is controlled using commands.

            There are three ways to run a command:
            - by typing the command in maestro’s command line (at the bottom of the app)
            - by binding a key to the command in the configuration file
            - by using the client program to send the command to the main application

            The idea is that you can bind the commands that you use often to a
            key, and access the other commands from the command-line.

            To see a documentation of available commands, see `help command`
            ''')


            @command("command", greedy_str_arg("command", default=''),
                     description='''
            Show help about a maestro command
            ''')
            def command_help(self, command: str):
                return self.get_command_help(command)

            @command("config", greedy_str_arg("option", default=''),
                     description='''
            Show help about maestro configuration options
            ''')
            def config_help(self, command: str):
                return self.configmanager.get_config_help(command)

            @command("advanced", description='Tips and tricks for advanced users')
            def tutorial_help(self):
                return make_doc_page(
            '''
            # Advanced tips and tricks

            ## Music tree

            ### Songs sorting

            By default, songs in an album are sorted in alphabetical order.
            If you want to define another order, you can prefix each song name
            with a number (this number is called an "index clue").
            Maestro will sort the songs based on that index (the index will only
            be used for sorting and will not be part of the song name).
            See also the config option `albums.use_index_clues`

            ### Album cover

            If you have multiple pictures in an album directory, maestro will
            use the first one it finds. However, if you name one of them with
            "cover" as the basename (e.g. "cover.png"), it will be used in
            priority.

            ## Client-server application

            Maestro is composed of two programs, a server application and a
            client.

            The server application opens the window application. It’s the one
            you usually uses. You launch it from your system menu or with the
            `maestroserver` executable.

            The client program is a cli application that communicates with the
            main application. You launch it with the `maestro` executable.
            It’s purpose is to display the documentation in the terminal or
            send commands to the main application (for scripting or interaction
            with other tools).
            ''')

            @command("iamlost", description='Help system overview')
            def intro_help(self):
                doc = make_doc_page(
            f'''
            # Maestro help

            If you have never used maestro before, see `help setup` and
            `help tutorial`

            You can also access the following help pages with `help <page-name>`
            ''')
                doc.add(self.get_command_help('help'))
                return doc

        @command('quit', description='Exit the application')
        def quit(self):
            self.view.stop()


    # Utilities --------------------------------------------------------------

    def start_playing_song(self):
        if self.model.playing_song.is_dummy:
            self.stop_playing()
        else:
            self.song_player.set_song(self.model.playing_song.path)
            self.song_player.play()
            self.show_playing_song(self.model.playing_song)
            self.show_current_panel()

    def show_playing_song(self, song: Song):
        self.view.set_playing_song(song.name, song.cover, song.album_name)
        self.show_queue_status()

    def show_current_panel(self):
        self.show_panel(self.model.current_panel.name)

    def show_queue_status(self):
        self.view.update_queue_status(self.model.playing_index,
                                      self.model.queue_length)

    def scan_collection(self):
        self.show_playing_song(Song.dummy())
        collection_directory = self.configmanager.ask_key('music_collection')
        if collection_directory == '':
            collection_directory = DEFAULT_COLLECTION_DIR
        path = Path(collection_directory).expanduser()
        if not path.exists():
            message = (f"path '{path.as_posix()}' does not exist, "
                       f"no music collection loaded")
            self.model.switch_to_mode(AppMode.POPUP)
            self.view.launch_error("Invalid config", message, fatal=True)
            return
        recurse = self.configmanager.ask_key('albums.recursive_search')
        collection = MusicCollection()
        collection.add_albums(scan_music_collection(path, recurse))
        collection.sort()
        self.model.set_collection(collection)
        self.show_panel('collection')
        self.collection_scan_success = True


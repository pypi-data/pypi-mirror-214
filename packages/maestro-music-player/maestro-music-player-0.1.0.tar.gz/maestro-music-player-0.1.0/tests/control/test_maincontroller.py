from maestro.control.maincontroller import MainController

from maestro.model.application import Application

import trio
from pathlib import Path
import shutil

import pytest

def interface(interface_desc: str):
    return interface_desc.strip()

def fake_uid_cache(parent_path, files):
    cache_dict = {}
    for i, file in enumerate(files):
        path = (parent_path / file).as_posix()
        cache_dict[path] = str(i)
    return cache_dict

@pytest.fixture
def dummy_view_class():
    class DummyView:

        def __init__(self, configmgr):
            self.panels = {}
            self.playing_song = ''
            self.queue_status = ''
            self.error_popup = None
            self.playing_progress = ''
            self.loop = ''
            self.volume = ''
            self.fatal_error = False
            self.is_closed = False

        @property
        def current_panel_columns(self):
            if self.central_panel == 'collection':
                return 2
            return 1

        @property
        def interface(self):
            first = f'{self.playing_song} | {self.playing_progress}'
            second = f'{self.queue_status} | {self.loop} | {self.volume}'
            panel = f'[{self.panels[self.central_panel]}]'
            if self.error_popup:
                return self.error_popup
            return '\n'.join([first, second, panel])

        def _item_repr(self, focused, playing):
            if playing:
                return '>'
            if focused:
                return 'x'
            return '.'

        def register_controller(self, controller):
            self.controller = controller

        def update_panel(self, panel_name: str, panel_data):
            if panel_name == 'documentation':
                return
            if panel_name == 'queue':
                playing_index = panel_data.playing_index
            else:
                playing_index = -1
            self.panels[panel_name] = ''.join(
                [self._item_repr(i == panel_data.focused_index,
                                 i == playing_index)
                 for i, item in enumerate(panel_data)]
            )

        def update_queue_status(self, playing_index, queue_length):
            index = "-" if playing_index is None else f"{playing_index+1}"
            self.queue_status = f"{index} / {queue_length}"

        def display_panel(self, panel_name: str):
            self.central_panel = panel_name

        def launch_error(self, title: str, error_message: str, fatal: bool = False,
                         external_source: bool = False):
            error = f'{title}: {error_message}'
            if external_source:
                return error
            self.error_popup = error
            if fatal:
                self.fatal_error = True

        def launch_info(self, message: str, external_source: bool = False):
            if external_source:
                return message
            self.error_popup = message

        def dismiss_popup(self):
            self.error_popup = None

        def set_playing_song(self, name: str, cover: str, album: str):
            self.playing_song = name

        def set_playing_progress(self, time, duration):
            self.playing_progress = f'{time} / {duration}'

        def set_loop_status(self, loop: bool):
            self.loop = 'on' if loop else 'off'

        def set_volume_level(self, volume: int):
            self.volume = str(volume)

        def command_line(self, focus, text=None):
            self.controller.command_line_focus_event(focus)

        def on_start(self):
            self.controller.app_start_event()
            self.ping_refresh(0)

        def ping_refresh(self, time):
            self.controller.ping_refresh()

        def on_stop(self):
            self.controller.close_app_event()
            self.is_closed = True

        def stop(self):
            self.on_stop()

        async def async_run(self):
            self.on_start()

        def show_doc_in_panel(self, doc):
            self.panels['documentation'] = doc.header.lines[0]

    return DummyView

@pytest.fixture
def dummy_sound_class():

    class DummySound:

        def __init__(self, backend):
            if backend not in ['mpv', 'vlc']:
                raise ValueError('invalid backend')
            self.is_idle = True
            self.is_paused = False
            self.time = 0
            self.duration = 0
            self.volume = 100
            self.song = None

        @property
        def is_playing_music(self):
            return not (self.is_idle or self.is_paused)

        def set_song(self, path: Path):
            self.time = 0
            self.duration = 0
            self.song = path.stem
            self.duration = 3

        def time_passes(self):
            if not (self.is_idle or self.is_paused):
                self.time += 1

        def ping(self):
            if self.time >= self.duration:
                self.stop()

        def set_volume(self, new_volume: int):
            self.volume = new_volume

        def increment_volume(self, increment: int):
            self.volume = max(0, min(100, self.volume+increment))

        def toggle_play_pause(self):
            if self.is_idle:
                self.play()
            else:
                self.is_paused = not self.is_paused

        def pause(self):
            self.is_paused = True

        def play(self):
            self.is_paused = False
            self.is_idle = False

        def stop(self):
            self.time = 0
            self.duration = 0
            self.is_idle = True
            self.is_paused = False

    return DummySound

@pytest.fixture
def time_passes(controller):
    def advance_time():
        controller.song_player.time_passes()
        controller.ping_refresh()
    return advance_time

@pytest.fixture
def no_config_file(tmp_path):
    return tmp_path / 'no_config_file.yaml'

@pytest.fixture
def valid_config(tmp_path):
    # prepare config file
    user_config = f'''
music_collection: {tmp_path.as_posix()}

keys:
    normal:
        l: focus move left
        r: focus move right
        d: focus move down
        u: focus move up
        q: show-panel queue
        c: show-panel collection
        a: show-panel album
'''
    config_path = tmp_path / 'user_config.yaml'
    with open(config_path, 'w') as file:
        file.write(user_config)
    return config_path

INVALID_CONFIGS = [
'''
music_collection: {}

keys:
    azsntdietnaust: 9
''',

'''
music_collection: {}

keys:
    normal:
        l: focus move zzz
''',

'''
music_collection: {}

audio:
    backend: magic-audio
''',

'''
music_collection: "a_totally_invalid_music_collection_path"

''',
]

@pytest.fixture(params=INVALID_CONFIGS)
def invalid_config(tmp_path, request):
    # prepare config file
    user_config = request.param.format(tmp_path.as_posix())
    config_path = tmp_path / 'user_config.yaml'
    with open(config_path, 'w') as file:
        file.write(user_config)
    return config_path

INVALID_THEMES_CONFIGS = [
'''
music_collection: {}

theme:
    name: 'zatdtausnatutesnatusenaess'
''',

'''
music_collection: {}

theme:
    name: '{broken_theme}'
''',

'''
music_collection: {}

theme:
    name: 'broken_theme'
''',
]

@pytest.fixture(params=INVALID_THEMES_CONFIGS)
def invalid_theme(tmp_path, request):
    # prepare config file
    theme_path = Path(__file__).parent / 'themes/broken_theme.yaml'
    user_config = request.param.format(tmp_path.as_posix(),
                                       broken_theme=theme_path)
    config_path = tmp_path / 'user_config.yaml'
    theme_dir = tmp_path / 'themes'
    theme_dir.mkdir()
    source = 'broken_theme.yaml'
    dest = theme_dir / 'broken_theme.yaml'
    shutil.copy(theme_path, dest)
    with open(config_path, 'w') as file:
        file.write(user_config)
    return config_path

@pytest.fixture
def empty_cache_file(tmp_path):
    fruits = tmp_path / 'fruits'
    fruits.mkdir()
    (fruits / 'pomme.ogg').touch()
    (fruits / 'poire.ogg').touch()
    (fruits / 'abricot.ogg').touch()
    (fruits / 'banane.ogg').touch()

    special = tmp_path / 'special'
    special.mkdir()
    (special / 'chocolat.opus').touch()
    (special / 'gateau.ogg').touch()

    v = tmp_path / 'v'
    v.mkdir()
    (v / 'v.mp3').touch()

    w = tmp_path / 'w'
    w.mkdir()
    (w / 'w.mp3').touch()

    x = tmp_path / 'x'
    x.mkdir()
    (x / 'x.mp3').touch()
    return tmp_path / 'does_not_exist.json'

@pytest.fixture
def cache_file(empty_cache_file, tmp_path):
    # prepare cache file
    # /!\ alphabetical order
    uid_cache = fake_uid_cache(tmp_path, [
        "fruits/abricot.ogg",
        "fruits/banane.ogg",
        "fruits/poire.ogg",
        "fruits/pomme.ogg",

        "special/chocolat.opus",
        "special/gateau.ogg",

        "v/v.mp3",
        "w/w.mp3",
        "x/x.mp3",
    ])

    cache_path = tmp_path / 'uids.json'
    import json
    with open(cache_path, 'w') as file:
        json.dump(uid_cache, file)

    return cache_path

@pytest.fixture
def controller(cache_file, valid_config,
               dummy_view_class, dummy_sound_class, tmp_path):
    # playlist
    playlist = '8\n5\n6'
    playlist_path = tmp_path / 'playlist.list'
    with open(playlist_path, 'w') as file:
        file.write(playlist)
    # prepare controller
    mc = MainController(model=Application,
                        view=dummy_view_class,
                        sound=dummy_sound_class,
                        user_config=valid_config,
                        cache_file=cache_file,
    )
    trio.run(run_controller, mc)
    return mc

@pytest.fixture
def controller_no_cache(empty_cache_file, valid_config,
                        dummy_view_class, dummy_sound_class, tmp_path):
    # prepare controller
    mc = MainController(model=Application,
                        view=dummy_view_class,
                        sound=dummy_sound_class,
                        user_config=valid_config,
                        cache_file=empty_cache_file,
    )
    trio.run(run_controller, mc)
    return mc

async def run_controller(controller):
    await controller.async_run()
    await controller.initialization_done.wait()

# ----------------------------------------------------------------------------
# default controller

@pytest.mark.trio
async def test_default_controller(cache_file, controller):
    assert cache_file.exists()
    assert controller.collection_scan_success
    assert not controller.model.songcache_was_modified
    controller.close_app_event()

# ----------------------------------------------------------------------------
# dummy controller
def test_dummy_controller(capsys):
    mc = MainController.dummy()
    mc.command_line_event('help', external_source=True)
    # Not working anymore since the doc is displayed by less
    # res = capsys.readouterr()
    # assert 'help' in res.out

# ----------------------------------------------------------------------------
# invalid config

def test_controller_no_config(cache_file, no_config_file,
                              dummy_view_class, dummy_sound_class,
                              tmp_path):
    # prepare controller
    mc = MainController(model=Application,
                        view=dummy_view_class,
                        sound=dummy_sound_class,
                        user_config=no_config_file,
                        cache_file=cache_file,
    )
    trio.run(run_controller, mc)
    assert mc.view.fatal_error

def test_controller_invalid_config(cache_file, invalid_config,
                                   dummy_view_class, dummy_sound_class,
                                   tmp_path):
    # prepare controller
    mc = MainController(model=Application,
                        view=dummy_view_class,
                        sound=dummy_sound_class,
                        user_config=invalid_config,
                        cache_file=cache_file,
    )
    trio.run(run_controller, mc)
    assert mc.view.fatal_error

def test_controller_invalid_theme(cache_file, invalid_theme,
                                  dummy_view_class, dummy_sound_class,
                                  tmp_path):
    # prepare controller
    mc = MainController(model=Application,
                        view=dummy_view_class,
                        sound=dummy_sound_class,
                        user_config=invalid_theme,
                        cache_file=cache_file,
    )
    trio.run(run_controller, mc)
    assert mc.view.error_popup is not None
    assert not mc.view.fatal_error

def test_on_fatal_error_do_not_destroy_the_cache(cache_file, invalid_config,
                                                 dummy_view_class,
                                                 dummy_sound_class,
                                                 tmp_path):

    # prepare controller
    mc = MainController(model=Application,
                        view=dummy_view_class,
                        sound=dummy_sound_class,
                        user_config=invalid_config,
                        cache_file=cache_file,
    )
    trio.run(run_controller, mc)

    cache_file.unlink()
    mc.command_line_event('quit')
    assert not cache_file.exists()
    assert mc.view.is_closed


def test_app_start_event(controller):
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 0 | off | 100
[x....]
''')
    assert not controller.song_player.is_playing_music


def test_app_starts_even_without_cache(controller_no_cache):
    assert controller_no_cache.view.interface == interface(
'''
nothing to play | 0 / 0
- / 0 | off | 100
[x....]
''')
    assert not controller_no_cache.song_player.is_playing_music

# ----------------------------------------------------------------------------
# app close

@pytest.mark.trio
async def test_close_command_closes_app_and_do_not_write_cache(cache_file, controller, tmp_path):
    cache_file.unlink()
    controller.command_line_event('quit')
    assert controller.collection_scan_success
    assert not controller.model.songcache_was_modified
    assert not cache_file.exists() # no cache file since cache did not changed
    assert controller.view.is_closed
    controller.close_app_event()

def test_close_command_closes_app_and_write_modified_cache(empty_cache_file, controller_no_cache, tmp_path):
    controller_no_cache.command_line_event('quit')
    assert controller_no_cache.collection_scan_success
    assert controller_no_cache.model.songcache_was_modified
    assert empty_cache_file.exists()
    assert controller_no_cache.view.is_closed

# ----------------------------------------------------------------------------
# playing and pausing 

@pytest.fixture
def setup_queue(controller, time_passes):
    controller.command_line_event('current add')

def test_pause_pauses_playing(controller, setup_queue, time_passes):
    controller.command_line_event('play')
    time_passes()
    assert controller.view.interface == interface(
'''
abricot | 1 / 3
1 / 4 | off | 100
[x....]
''')
    assert controller.song_player.is_playing_music
    controller.command_line_event('pause')
    time_passes()
    time_passes()
    assert controller.view.interface == interface(
'''
abricot | 1 / 3
1 / 4 | off | 100
[x....]
''')
    assert not controller.song_player.is_playing_music
    controller.command_line_event('play')
    time_passes()
    assert controller.view.interface == interface(
'''
abricot | 2 / 3
1 / 4 | off | 100
[x....]
''')
    assert controller.song_player.is_playing_music
    controller.command_line_event('pause')
    time_passes()
    assert controller.view.interface == interface(
'''
abricot | 2 / 3
1 / 4 | off | 100
[x....]
''')

def test_play_pause_toggles_playing(controller, setup_queue, time_passes):
    controller.command_line_event('play-pause')
    time_passes()
    assert controller.view.interface == interface(
'''
abricot | 1 / 3
1 / 4 | off | 100
[x....]
''')
    assert controller.song_player.is_playing_music
    controller.command_line_event('play-pause')
    time_passes()
    time_passes()
    assert controller.view.interface == interface(
'''
abricot | 1 / 3
1 / 4 | off | 100
[x....]
''')
    assert not controller.song_player.is_playing_music
    controller.command_line_event('play-pause')
    time_passes()
    assert controller.view.interface == interface(
'''
abricot | 2 / 3
1 / 4 | off | 100
[x....]
''')
    assert controller.song_player.is_playing_music
    controller.command_line_event('play-pause')
    time_passes()
    assert controller.view.interface == interface(
'''
abricot | 2 / 3
1 / 4 | off | 100
[x....]
''')

def test_double_play_continues_to_play(controller, setup_queue, time_passes):
    controller.command_line_event('play')
    assert controller.song_player.is_playing_music
    time_passes()
    controller.command_line_event('play')
    assert controller.song_player.is_playing_music
    time_passes()

def test_double_pause_continues_to_pause(controller, setup_queue, time_passes):
    controller.command_line_event('play')
    assert controller.song_player.is_playing_music
    time_passes()
    controller.command_line_event('pause')
    assert not controller.song_player.is_playing_music
    time_passes()
    controller.command_line_event('pause')
    assert not controller.song_player.is_playing_music
    time_passes()

def test_play_plays_first_album(controller, setup_queue, time_passes):
    controller.command_line_event('play')
    time_passes()
    assert controller.song_player.is_playing_music
    assert controller.view.interface == interface(
'''
abricot | 1 / 3
1 / 4 | off | 100
[x....]
''')

def test_play_pause_plays_first_album(controller, setup_queue, time_passes):
    controller.command_line_event('play-pause')
    time_passes()
    assert controller.song_player.is_playing_music
    assert controller.view.interface == interface(
'''
abricot | 1 / 3
1 / 4 | off | 100
[x....]
''')

def test_music_changes_when_time_passes(controller, setup_queue, time_passes):
    controller.command_line_event('play')
    time_passes()
    time_passes()
    assert controller.song_player.is_playing_music
    assert controller.view.interface == interface(
'''
abricot | 2 / 3
1 / 4 | off | 100
[x....]
''')
    time_passes()
    assert controller.song_player.is_playing_music
    assert controller.view.interface == interface(
'''
banane | 0 / 0
2 / 4 | off | 100
[x....]
''')
    time_passes()
    assert controller.song_player.is_playing_music
    assert controller.view.interface == interface(
'''
banane | 1 / 3
2 / 4 | off | 100
[x....]
''')

# ----------------------------------------------------------------------------
# get information

def test_get_information_external(controller, setup_queue):
    controller.command_line_event('play')
    assert controller.command_line_event('get playing-title') == 'abricot'

def test_get_information_internal(controller, setup_queue):
    controller.command_line_event('play')
    controller.command_line_event('get playing-title', external_source=False)
    assert controller.view.interface == interface('abricot')

# ----------------------------------------------------------------------------
# set focus

def test_set_focus_in_empty_panel(controller):
    controller.command_line_event('show-panel album')
    controller.command_line_event('focus set top')
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 0 | off | 100
[]
''')
    controller.command_line_event('focus set bottom')
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 0 | off | 100
[]
''')

def test_set_focus_in_queue(controller, setup_queue):
    controller.keypress_event((0, 'q'), [])
    controller.keypress_event((0, 'd'), [])
    controller.keypress_event((0, 'd'), [])
    controller.command_line_event('focus set playing')
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 4 | off | 100
[..x.]
''')
    assert not controller.song_player.is_playing_music
    controller.command_line_event('current play')
    assert controller.view.interface == interface(
'''
poire | 0 / 0
3 / 4 | off | 100
[..>.]
''')
    assert controller.song_player.is_playing_music
    controller.command_line_event('focus set bottom')
    assert controller.view.interface == interface(
'''
poire | 0 / 0
3 / 4 | off | 100
[..>x]
''')
    assert controller.song_player.is_playing_music
    controller.command_line_event('focus set top')
    assert controller.view.interface == interface(
'''
poire | 0 / 0
3 / 4 | off | 100
[x.>.]
''')
    assert controller.song_player.is_playing_music
    controller.command_line_event('focus set playing')
    assert controller.view.interface == interface(
'''
poire | 0 / 0
3 / 4 | off | 100
[..>.]
''')
    assert controller.song_player.is_playing_music

# ----------------------------------------------------------------------------
# clear queue

def test_clear_queue(controller, setup_queue, time_passes):
    controller.command_line_event('show-panel queue')
    controller.command_line_event('play')
    time_passes()
    assert controller.view.interface == interface(
'''
abricot | 1 / 3
1 / 4 | off | 100
[>...]
''')
    assert controller.song_player.is_playing_music
    controller.command_line_event('queue clear')
    time_passes()
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 0 | off | 100
[]
''')
    assert not controller.song_player.is_playing_music

# ----------------------------------------------------------------------------
# command line focus

def test_focus_and_unfocusing_cmdline_goes_back_to_normal_mode(controller):
    controller.command_line_event('command-line focus')
    controller.keypress_event((0, 'r'), [])
    controller.keypress_event((0, 'r'), [])
    controller.keypress_event((0, 'r'), [])
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 0 | off | 100
[x....]
''')
    controller.command_line_event('command-line leave')
    controller.keypress_event((0, 'r'), [])
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 0 | off | 100
[.x...]
''')

def test_focus_and_clear_cmdline_goes_back_to_normal_mode(controller):
    controller.command_line_event('command-line focus')
    controller.keypress_event((0, 'r'), [])
    controller.keypress_event((0, 'r'), [])
    controller.keypress_event((0, 'r'), [])
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 0 | off | 100
[x....]
''')
    controller.command_line_event('command-line clear')
    controller.keypress_event((0, 'r'), [])
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 0 | off | 100
[.x...]
''')

# ----------------------------------------------------------------------------
# error management

def test_invalid_command_external(controller):
    message = controller.command_line_event('zaiuzeatpentsainuetanu')
    assert message.startswith('Invalid command')

def test_invalid_command_internal(controller):
    controller.command_line_event('zaiuzeatpentsainuetanu',
                                  external_source=False)
    assert controller.view.interface.startswith('Invalid command')

def test_dismiss_popup(controller):
    controller.command_line_event('zaiuzeatpentsainuetanu',
                                  external_source=False)
    assert controller.view.interface.startswith('Invalid command')
    controller.keypress_event((0, 'r'), [])
    assert controller.view.interface.startswith('Invalid command')
    controller.command_line_event('dismiss-popup')
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 0 | off | 100
[x....]
''')
    controller.command_line_event('dismiss-popup')
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 0 | off | 100
[x....]
''')

def test_print_keycodes(controller):
    controller.command_line_event('print-keycodes',
                                  external_source=False)
    assert 'key' in controller.view.interface
    controller.keypress_event((0, 'r'), ['ctrl'])
    assert 'ctrl-r' in controller.view.interface
    controller.command_line_event('dismiss-popup')
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 0 | off | 100
[x....]
''')

# ----------------------------------------------------------------------------
# move focus

def test_move_focus_with_keys(controller):
    controller.keypress_event((0, 'r'), [])
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 0 | off | 100
[.x...]
''')
    controller.keypress_event((0, 'r'), [])
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 0 | off | 100
[..x..]
''')
    controller.keypress_event((0, 'd'), [])
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 0 | off | 100
[....x]
''')
    controller.keypress_event((0, 'r'), [])
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 0 | off | 100
[....x]
''')
    controller.keypress_event((0, 'u'), [])
    controller.keypress_event((0, 'u'), [])
    controller.keypress_event((0, 'u'), [])
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 0 | off | 100
[x....]
''')

# ----------------------------------------------------------------------------
# move focus

def test_play_next_previous(controller, setup_queue, time_passes):
    controller.command_line_event('play')
    time_passes()
    controller.keypress_event((0, 'q'), [])
    assert controller.view.interface == interface(
'''
abricot | 1 / 3
1 / 4 | off | 100
[>...]
''')
    assert controller.song_player.is_playing_music
    controller.command_line_event('next')
    time_passes()
    assert controller.view.interface == interface(
'''
banane | 1 / 3
2 / 4 | off | 100
[x>..]
''')
    assert controller.song_player.is_playing_music
    controller.command_line_event('next')
    controller.command_line_event('next')
    time_passes()
    assert controller.view.interface == interface(
'''
pomme | 1 / 3
4 / 4 | off | 100
[x..>]
''')
    assert controller.song_player.is_playing_music
    controller.command_line_event('previous')
    time_passes()
    assert controller.view.interface == interface(
'''
poire | 1 / 3
3 / 4 | off | 100
[x.>.]
''')
    assert controller.song_player.is_playing_music
    controller.command_line_event('next')
    controller.command_line_event('next')
    time_passes()
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 4 | off | 100
[x...]
''')
    assert not controller.song_player.is_playing_music

# ----------------------------------------------------------------------------
# stop playing

def test_stop_playing(controller, setup_queue, time_passes):
    controller.command_line_event('next')
    controller.command_line_event('next')
    time_passes()
    controller.keypress_event((0, 'q'), [])
    assert controller.view.interface == interface(
'''
banane | 1 / 3
2 / 4 | off | 100
[x>..]
''')
    assert controller.song_player.is_playing_music
    controller.command_line_event('stop')
    time_passes()
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 4 | off | 100
[x...]
''')
    assert not controller.song_player.is_playing_music

# ----------------------------------------------------------------------------
# show panel

def test_show_panel(controller):
    controller.keypress_event((0, 'r'), [])
    controller.command_line_event('current show')
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 0 | off | 100
[x.]
''')
    controller.command_line_event('current show')
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 0 | off | 100
[x.]
''')
    controller.command_line_event('current add')
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 1 | off | 100
[x.]
''')
    controller.keypress_event((0, 'q'), [])
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 1 | off | 100
[x]
''')
    controller.keypress_event((0, 'c'), [])
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 1 | off | 100
[.x...]
''')
    controller.keypress_event((0, 'r'), [])
    controller.command_line_event('current show')
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 1 | off | 100
[x]
''')

# ----------------------------------------------------------------------------
# loop

def test_set_loop(controller, time_passes):
    controller.keypress_event((0, 'r'), [])
    controller.keypress_event((0, 'r'), [])
    controller.command_line_event('current add')
    controller.keypress_event((0, 'r'), [])
    controller.command_line_event('current add')
    controller.keypress_event((0, 'q'), [])
    controller.command_line_event('play')
    time_passes()
    time_passes()
    assert controller.view.interface == interface(
'''
v | 2 / 3
1 / 2 | off | 100
[>.]
''')
    assert controller.song_player.is_playing_music
    controller.command_line_event('next')
    controller.command_line_event('loop on')
    time_passes()
    assert controller.view.interface == interface(
'''
w | 1 / 3
2 / 2 | on | 100
[x>]
''')
    assert controller.song_player.is_playing_music
    time_passes()
    time_passes()
    assert controller.view.interface == interface(
'''
v | 0 / 0
1 / 2 | on | 100
[>.]
''')
    assert controller.song_player.is_playing_music
    controller.command_line_event('previous')
    assert controller.view.interface == interface(
'''
w | 0 / 0
2 / 2 | on | 100
[x>]
''')
    assert controller.song_player.is_playing_music

# ----------------------------------------------------------------------------
# selection

def test_selection(controller):
    controller.command_line_event('select current')
    controller.command_line_event('selection add')
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 4 | off | 100
[x....]
''')
    controller.command_line_event('select all')
    controller.command_line_event('selection add')
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 13 | off | 100
[x....]
''')
    controller.command_line_event('play')
    assert controller.song_player.is_playing_music
    controller.command_line_event('deselect current')
    controller.command_line_event('selection add')
    assert controller.view.interface == interface(
'''
abricot | 0 / 0
1 / 18 | off | 100
[x....]
''')
    # removing works only in queue panel
    controller.command_line_event('selection remove')
    assert controller.view.interface == interface(
'''
abricot | 0 / 0
1 / 18 | off | 100
[x....]
''')
    controller.command_line_event('show-panel queue')
    controller.command_line_event('focus move down')
    controller.command_line_event('toggle-select current')
    controller.command_line_event('toggle-select all')
    assert controller.song_player.is_playing_music
    controller.command_line_event('selection remove')
    assert not controller.song_player.is_playing_music
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 1 | off | 100
[x]
''')
    controller.command_line_event('deselect all')
    controller.command_line_event('selection remove')
    assert not controller.song_player.is_playing_music
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 1 | off | 100
[x]
''')

# ----------------------------------------------------------------------------
# volume

def test_volume(controller, time_passes):
    controller.command_line_event('current add')
    controller.command_line_event('play')
    time_passes()
    assert controller.view.interface == interface(
'''
abricot | 1 / 3
1 / 4 | off | 100
[x....]
''')
    assert controller.song_player.is_playing_music
    assert controller.song_player.volume == 100
    controller.command_line_event('volume set 30')
    assert controller.view.interface == interface(
'''
abricot | 1 / 3
1 / 4 | off | 30
[x....]
''')
    assert controller.song_player.is_playing_music
    assert controller.song_player.volume == 30
    controller.command_line_event('volume increment 30')
    assert controller.view.interface == interface(
'''
abricot | 1 / 3
1 / 4 | off | 60
[x....]
''')
    assert controller.song_player.is_playing_music
    assert controller.song_player.volume == 60
    controller.command_line_event('volume decrement 15')
    assert controller.view.interface == interface(
'''
abricot | 1 / 3
1 / 4 | off | 45
[x....]
''')
    assert controller.song_player.is_playing_music
    assert controller.song_player.volume == 45

# ----------------------------------------------------------------------------
# playlist

@pytest.mark.trio
async def test_playlist(controller, tmp_path):
    # wait for the uid cache to be ready
    await controller.uids_computed.wait()
    playlist_path = (tmp_path / 'playlist.list').as_posix()
    controller.command_line_event(f'playlist load {playlist_path}')
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 3 | off | 100
[x....]
''')
    controller.command_line_event(f'playlist load {playlist_path}')
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 6 | off | 100
[x....]
''')
    controller.command_line_event(f'playlist save {playlist_path}')
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 6 | off | 100
[x....]
''')
    controller.command_line_event(f'queue clear')
    controller.command_line_event(f'playlist load {playlist_path}')
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 6 | off | 100
[x....]
''')
    controller.close_app_event()

# This test is disabled for now as it’s not deterministic enough
# We should add a way to make sure uids are NOT computed to test this
# in a reliable way

# @pytest.mark.trio
# async def test_load_playlist_when_uids_are_not_computed(controller, tmp_path):
#     playlist_path = (tmp_path / 'playlist.list').as_posix()
#     res = controller.command_line_event(f'playlist load {playlist_path}',
#                                         external_source=True)
#     assert 'indexing' in res
#     controller.close_app_event()

def test_load_invalid_playlist(controller, tmp_path):
    playlist_path = (tmp_path / 'does_not_exist.list').as_posix()
    controller.command_line_event(f'playlist load {playlist_path}', external_source=False)
    assert controller.view.interface.startswith('Invalid command')

# ----------------------------------------------------------------------------
# shuffle queue

def test_shuffle_queue(controller):
    controller.command_line_event('current add')
    controller.keypress_event((0, 'q'), [])
    controller.keypress_event((0, 'd'), [])
    controller.keypress_event((0, 'd'), [])
    controller.command_line_event('current play')
    assert controller.view.interface == interface(
'''
poire | 0 / 0
3 / 4 | off | 100
[..>.]
''')
    assert controller.song_player.is_playing_music
    controller.command_line_event('queue shuffle')
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 4 | off | 100
[x...]
''')
    assert not controller.song_player.is_playing_music

# ----------------------------------------------------------------------------
# action on current

def test_select_first_album(controller):
    controller.command_line_event('current show')
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 0 | off | 100
[x...]
''')
    assert not controller.song_player.is_playing_music

def test_show_first_song_in_queue(controller):
    controller.command_line_event('current add')
    controller.command_line_event('show-panel queue')
    controller.command_line_event('current show')
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 4 | off | 100
[x...]
''')
    assert not controller.song_player.is_playing_music

def test_current_remove_from_queue(controller):
    controller.command_line_event('current add')
    controller.command_line_event('current play')
    controller.command_line_event('current remove')
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 4 | off | 100
[x....]
''')
    controller.command_line_event('show-panel queue')
    assert not controller.song_player.is_playing_music
    controller.command_line_event('current play')
    assert controller.song_player.is_playing_music
    assert controller.view.interface == interface(
'''
abricot | 0 / 0
1 / 4 | off | 100
[>...]
''')
    controller.command_line_event('current remove')
    assert not controller.song_player.is_playing_music
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 3 | off | 100
[x..]
''')

# ----------------------------------------------------------------------------
# documentation

def test_show_documentation_in_app(controller):
    controller.command_line_event('help command', external_source=False)
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 0 | off | 100
[List of commands for maestro:]
''')
    controller.command_line_event('show-panel documentation', external_source=False)
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 0 | off | 100
[List of commands for maestro:]
''')
    controller.command_line_event('current show')
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 0 | off | 100
[List of commands for maestro:]
''')
    controller.command_line_event('help config', external_source=False)
    assert controller.view.interface == interface(
'''
nothing to play | 0 / 0
- / 0 | off | 100
[Maestro configuration file]
''')

def test_various_documentation_pages_do_not_crash(controller):
    controller.command_line_event('help')
    controller.command_line_event('help iamlost')
    controller.command_line_event('help setup')
    controller.command_line_event('help tutorial')
    controller.command_line_event('help advanced')

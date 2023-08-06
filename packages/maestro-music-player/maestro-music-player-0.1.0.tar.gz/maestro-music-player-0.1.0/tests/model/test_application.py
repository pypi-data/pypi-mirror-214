from maestro.model.application import Application
from maestro.model.collection import Song, Album, MusicCollection

from pathlib import Path

import pytest

@pytest.fixture
def app():
    cache = {
        'apple.ogg': 1,
        'banana.ogg': 2,
        'lemon.ogg': 3,
        'orange.ogg': 4,
        'white.ogg': 5,
        'milk.ogg': 6,
        'dark.ogg': 7,
    }

    fruits = Album("Fruits")
    apple = Song(Path("apple.ogg"), fruits)
    banana = Song(Path("banana.ogg"), fruits)
    lemon = Song(Path("lemon.ogg"), fruits)
    orange = Song(Path("orange.ogg"), fruits)
    fruits.append(apple)
    fruits.append(banana)
    fruits.append(lemon)
    fruits.append(orange)

    chocolate = Album("Chocolate")
    white = Song(Path("white.ogg"), chocolate)
    milk = Song(Path("milk.ogg"), chocolate)
    dark = Song(Path("dark.ogg"), chocolate)
    chocolate.append(white)
    chocolate.append(milk)
    chocolate.append(dark)

    Song.set_cache(cache)

    collection = MusicCollection()
    collection.add_album(fruits)
    collection.add_album(chocolate)

    new_app = Application()
    new_app.set_collection(collection)
    return new_app

def test_uid_cache_get_and_set(app):
    cache = app.get_songuid_cache()
    assert type(cache) == dict
    app.load_songuid_cache(cache)

def test_set_invalid_uid_cache_raises_exception(app):
    cache = [('whatever', 0), ('another', 1)]
    with pytest.raises(Exception):
        app.load_songuid_cache(cache)

def test_selection_in_collection(app):
    app.show_panel('collection')
    app.current_panel.select_all(invert=True)
    app.add_selection_to_queue()
    assert app.queue_length == 7

def test_selection_in_album_and_queue_panels(app):
    app.show_panel('collection')
    app.show_album_in_album_panel(app.focused_item)
    app.show_panel('album')
    app.current_panel.select_all(select=True)
    app.current_panel.select_focused(select=False)
    app.add_selection_to_queue()
    assert app.queue_length == 3
    app.show_panel('queue')
    app.move_focus(1)
    app.current_panel.select_focused(select=True)
    app.move_focus(1)
    app.current_panel.select_focused(select=True)
    app.current_panel.delete_selected()
    assert app.queue_length == 1
    assert app.focused_item.name == 'banana'
    app.current_panel.delete_focused()
    assert app.queue_length == 0

def test_set_indexes(app):
    app.show_panel('collection')
    app.focused_index = 1
    app.add_focused_to_queue()
    app.playing_index = 2
    assert app.playing_song.name == 'dark'

def test_loop_the_queue(app):
    app.show_panel('collection')
    app.add_focused_to_queue()
    app.loop = True
    assert app.loop
    app.play_next()
    assert app.playing_index == 0
    app.play_previous()
    assert app.playing_index == 3
    app.play_next()
    assert app.playing_index == 0
    app.loop = False
    assert not app.loop
    app.play_previous()
    assert app.playing_index is None

def test_application_get_collection():
    app = Application()
    collection = MusicCollection()
    app.set_collection(collection)
    assert app.collection is collection

def test_show_panel(app):
    app.show_panel('collection')
    assert app.current_panel.name == 'collection'
    assert app.focused_item.name == "Fruits"
    app.show_panel('album')
    assert app.current_panel.name == 'album'
    assert app.focused_item.is_dummy
    app.show_panel('queue')
    assert app.current_panel.name == 'queue'
    assert app.focused_item.is_dummy
    assert app.playing_song.is_dummy
    with pytest.raises(ValueError):
        app.show_panel('garbage')

def test_focus_next_album(app):
    app.show_panel('collection')
    assert app.focused_item.name == "Fruits"
    assert app.focused_index == 0
    app.move_focus(1)
    assert app.focused_item.name == "Chocolate"
    assert app.focused_index == 1

def test_show_album(app):
    app.show_panel('collection')
    assert app.focused_item.name == "Fruits"
    app.show_panel('album')
    assert app.focused_item.is_dummy
    app.show_panel('collection')
    app.show_album_in_album_panel(app.focused_item)
    app.show_panel('album')
    assert app.focused_item.name == "apple"

def test_show_next_song(app):
    app.show_album_in_album_panel(app.focused_item)
    app.show_panel('album')
    app.move_focus(2)
    assert app.focused_item.name == "lemon"

def test_add_to_queue(app):
    app.show_panel('collection')
    assert app.queue_length == 0
    app.add_focused_to_queue()
    assert app.queue_length == 4
    app.move_focus(1)
    app.show_album_in_album_panel(app.focused_item)
    app.show_panel('album')
    app.add_focused_to_queue()
    assert app.queue_length == 5
    app.add_focused_to_queue()
    assert app.queue_length == 6

def test_stop_playing(app):
    app.show_panel('collection')
    app.add_focused_to_queue()
    app.add_focused_to_queue()
    assert app.queue_length == 8
    app.play_next()
    app.play_next()
    app.play_next()
    assert app.playing_song.name == 'lemon'
    app.stop_playing()
    assert app.queue_length == 8
    assert app.playing_song.is_dummy

def test_clear_queue(app):
    app.show_panel('collection')
    app.add_focused_to_queue()
    app.add_focused_to_queue()
    assert app.queue_length == 8
    app.play_next()
    app.play_next()
    app.play_next()
    assert app.playing_song.name == 'lemon'
    app.clear_queue()
    assert app.queue_length == 0
    assert app.playing_song.is_dummy

def test_shuffle_queue(app):
    app.show_panel('collection')
    app.add_focused_to_queue()
    app.add_focused_to_queue()
    assert app.queue_length == 8
    app.shuffle_queue()
    assert app.queue_length == 8

def test_play_next_and_previous(app):
    app.show_panel('collection')
    app.add_focused_to_queue()
    app.play_next()
    assert app.playing_song.name == 'apple'
    assert app.playing_index == 0
    app.play_next()
    assert app.playing_song.name == 'banana'
    assert app.playing_index == 1
    app.play_next()
    assert app.playing_song.name == 'lemon'
    assert app.playing_index == 2
    app.play_next()
    assert app.playing_song.name == 'orange'
    assert app.playing_index == 3
    app.play_next()
    assert app.playing_song.is_dummy
    assert app.playing_index is None
    app.play_previous()
    assert app.playing_song.name == 'orange'
    assert app.playing_index == 3
    app.move_focus(1)
    app.show_album_in_album_panel(app.focused_item)
    app.show_panel('album')
    app.add_focused_to_queue()
    app.add_focused_to_queue()
    app.play_next()
    assert app.playing_song.name == 'white'
    app.play_next()
    assert app.playing_song.name == 'white'
    app.play_previous()
    app.play_previous()
    app.play_previous()
    assert app.playing_song.name == 'lemon'

